
### 📌 Overview

This repository serves as a technical sandbox for researching, documenting, and implementing advanced solutions in Network infrastructure, System automation, and On-premise services.

#### 1. Network Infrastructure

* **MPLS L3VPN Data Forwarding (Branch to HO):**
* *Use Case:* Ensuring secure, isolated, and fast communication between Branch Offices (e.g., Branch A) and Head Office (Vcenter) without exposing internal private IP routes to the ISP Core routers.
* *Problem/Scenario:* A User PC in Branch A (VLAN 16) wants to access a Virtual Machine (VM) hosted on the Vcenter at Head Office. How does the packet traverse the complex ISP MPLS network without traditional IP routing lookups at every hop?
* *Diagram:*

```mermaid
graph TD
    %% System color definitions
    classDef isp fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef fw fill:#ffcdd2,stroke:#c62828,stroke-width:2px;
    classDef core fill:#b3e5fc,stroke:#0277bd,stroke-width:2px;
    classDef providerA fill:#f0f4c3,stroke:#827717,stroke-width:1px;
    classDef providerB fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px;

    %% WAN ISP Providers
    subgraph ISPs ["WAN ISP Providers to Firewall"]
        ISP_A((Provider A WAN))
        ISP_B((Provider B WAN))
        ISP_C((Provider C WAN))
    end

    %% HEAD OFFICE
    subgraph HO ["Head Office - Enterprise Cluster"]
        FW["Firewall (Sophos / FortiGate)<br/>LAN IP: 192.168.10.10<br/>Security gateway to WAN"]
        
        CoreHO["Core Switch 3650<br/>Routing IP: 192.168.10.20<br/>(Routing enabled for internal traffic)"]
        
        BranchCore["Branch Core Switch<br/>IP: 192.168.1.10<br/>Handles branch VLAN routing"]
        
        Synology[(Storage System)]
        Vcenter_4Host[[Vcenter Cluster<br/>4 Hosts & VMs]]
    end

    %% MPLS TRANSPORT BACKBONE
    subgraph Transport ["WAN/MPLS Transport Backbone"]
        MPLS_A["Provider A MPLS Transport<br/>(Metro area coverage)"]
        
        MPLS_B["Provider B MPLS Transport<br/>(National coverage)"]
    end

    %% BRANCHES VIA PROVIDER A
    subgraph ProviderA_Branches ["Branches via Provider A MPLS"]
        subgraph BranchA ["Branch A"]
            PC_A["User PC A<br/>(VLAN 17)"]
            SW_A[Access Switch A]
        end
        BranchB["Branch B"]
        BranchC["Branch C"]
        BranchD["Branch D"]
    end

    %% BRANCHES VIA PROVIDER B
    subgraph ProviderB_Branches ["Branches via Provider B MPLS"]
        subgraph BranchE ["Branch E"]
            SW_E[Access Switch E]
            VLAN_102((VLAN 102)) --- SW_E
        end
        
        subgraph BranchF ["Branch F"]
            SW_F[Access Switch F]
            VLAN_168((VLAN 168)) --- SW_F
        end

        subgraph BranchG ["Branch G"]
            SW_G[Access Switch G]
            VLAN_157((VLAN 157)) --- SW_G
        end
        
        OtherProviderB["Other regional branches"]
    end

    %% PHYSICAL CONNECTIONS AND TRUNK/LACP DETAILS
    ISP_A --> FW
    ISP_B --> FW
    ISP_C --> FW
    CoreHO --- Synology
    CoreHO -- "Internal routing connection" --> BranchCore
    
    %% DEFAULT ROUTE TO INTERNET
    CoreHO -- "Default Route (0.0.0.0/0) to Internet" --> FW
    
    MPLS_A -.-> BranchB
    MPLS_A -.-> BranchC
    MPLS_A -.-> BranchD
    MPLS_B -.-> OtherProviderB

    %% 1. Core HO connection to Provider A MPLS via port pair
    CoreHO ===|interface GigabitEthernet1/0/44 & 1/0/45<br/>switchport mode trunk<br/>channel-protocol lacp<br/>channel-group 1 mode active| MPLS_A

    %% 2. Branch core connection to Provider B MPLS via port pair
    BranchCore ===|interface GigabitEthernet1/0/19 & 1/0/20<br/>switchport trunk encapsulation dot1q<br/>switchport mode trunk<br/>channel-group 1 mode active| MPLS_B

    %% PACKET FLOW ILLUSTRATION
    
    %% [RED PATH]: Provider A example from Branch A
    PC_A == "(1) Send IP Packet<br/>Src: VLAN 17 -> Dst: VM" ==> SW_A
    SW_A == "(2) Forward over Provider A MPLS" ==> MPLS_A
    MPLS_A == "(3) Remove MPLS label -> Enter channel group 1" ==> CoreHO

    %% [BLUE PATH]: Provider B example from Branch E
    VLAN_102 == "(A) Send IP Packet<br/>Src: VLAN 102 -> Dst: VM" ==> SW_E
    SW_E == "(B) Label and push into backbone" ==> MPLS_B
    MPLS_B == "(C) MPLS label switch to HO" ==> BranchCore
    BranchCore == "(D) Forward to Core HO" ==> CoreHO

    %% [COMMON PATH AT HO]: Core switch performs L3 routing
    CoreHO == "(4 / E) Receive and route traffic (L3 Routing)<br/>Forward directly to servers" ==> Vcenter_4Host

    %% PROVIDER PHYSICAL PE CONNECTION TO FIREWALL
    MPLS_B -. "Provider edge switch uplink<br/>(Two physical WAN lines to Sophos / FortiGate)" .-> ISP_B

    %% Component style assignment
    class ISP_A,ISP_B,ISP_C,MPLS_A,MPLS_B isp;
    class FW fw;
    class CoreHO,BranchCore core;
    class BranchA,BranchB,BranchC,BranchD providerA;
    class BranchE,BranchF,BranchG,OtherProviderB providerB;
    
    %% PACKET FLOW STYLES
    %% Provider A path (red)
    linkStyle 14,15,16 stroke:#ff1744,stroke-width:4px;
    
    %% Provider B path (blue)
    linkStyle 17,18,19,20 stroke:#2979ff,stroke-width:4px;
    
    %% Common L3 routing path at Core (purple)
    linkStyle 21 stroke:#9c27b0,stroke-width:4px;
```

* **VLAN Leaking & Layer 2 Loops:**
  * *Use Case:* Preventing broadcast storms in enterprise environments using STP and proper VLAN tagging. 
  * *Problem:* The PC in the Consulting Room belongs to VLAN 150, but it ultimately received an IP address from VLAN 204, which is designated for a different range.
  * *Diagram:*
```mermaid
sequenceDiagram
    autonumber
    participant PC as PC (Consulting Room)
    participant SW_TRET as Ground Floor SW (VLAN 150)
    participant SW_CORE as Branch Core SW
    participant SW_L1 as 1st Floor SW (VLAN 150, 204)
    participant SW_VT as IT Room SW (LOOPED)
    participant HO as HO Core (DHCP Server)

    Note over PC, HO: STEP 1: DHCP DISCOVER LEAKAGE (VLAN LEAKING) & BROADCAST DOMAIN MERGING
    
    rect rgba(0, 150, 255, 0.1)
        PC->>SW_TRET: Send DHCP Discover (Broadcast)
        SW_TRET->>SW_CORE: Forward to Branch Core SW (VLAN 150)
    end
    
    par Normal VLAN 150 Processing
        rect rgba(0, 150, 255, 0.1)
            SW_CORE->>HO: IP Helper 150 (Set giaddr=150.x): Request IP in 150 subnet
        end
    and Leakage via 1st Floor (Loop Error)
        rect rgba(255, 100, 100, 0.1)
            SW_CORE->>SW_L1: L2 Flood: Forward Broadcast to 1st Floor SW (VLAN 150)
            SW_L1->>SW_VT: Forward out port Gi0/1 (VLAN 150)
            Note over SW_L1, SW_VT: ⚠️ BROADCAST DOMAIN MERGING ERROR:<br/>IT Room SW lacks STP, floods Broadcast<br/>breaking through VLAN boundaries!
            SW_VT->>SW_L1: Broadcast packet loops back to port Gi0/8 (VLAN 204)
            SW_L1->>SW_CORE: Forward Broadcast back to Core SW (VLAN 204)
            SW_CORE->>HO: IP Helper 204 (Set giaddr=204.y): Request IP in 204 subnet
        end
    end

    Note over PC, HO: STEP 2: DHCP OFFER & RACE CONDITION (RFC 2131)
    HO->>SW_CORE: Server Replies with Offer IP 150.x
    HO->>SW_CORE: Server Replies with Offer IP 204.y
    
    par Normal Return Path (IP 150)
        rect rgba(0, 150, 255, 0.1)
            SW_CORE->>SW_TRET: Forward directly to Ground Floor SW
            SW_TRET->>PC: PC receives Offer 150 (Arrives later due to Processing Delay)
        end
    and Return Path via LOOP (IP 204)
        rect rgba(255, 100, 100, 0.1)
            SW_CORE->>SW_L1: Forward Offer 204.y to 1st Floor
            SW_L1->>SW_VT: Forward to IT Room SW (Gi0/8)
            SW_VT->>SW_L1: Loop back to VLAN 150 (Gi0/1)
            SW_L1->>SW_CORE: Loop back to Core SW (VLAN 150)
            SW_CORE->>SW_TRET: Core SW forwards to Ground Floor SW
            SW_TRET->>PC: PC receives Offer 204 (Arrives first!)
        end
    end

    Note over PC: DHCP Standard (RFC 2131): "First come, first served"<br/>PC decides to accept IP 204.y because it arrives first!

    Note over PC, HO: STEP 3 & 4: REQUEST & ACK (Packets continue to loop)
    
    rect rgba(0, 150, 255, 0.1)
        PC->>SW_TRET: DHCP Request: "Accept IP 204.y" (Still Broadcast)
        SW_TRET->>SW_CORE: Forward to Core SW (VLAN 150)
    end
    
    Note over SW_CORE, SW_VT: Core SW ignores Request on VLAN 150 (requesting IP 204).<br/>However, the Request packet is flooded again through the LOOP path!
    
    rect rgba(255, 100, 100, 0.1)
        SW_CORE->>SW_L1: Flood to 1st Floor (VLAN 150)
        SW_L1->>SW_VT: Forward to IT Room SW (Gi0/1)
        SW_VT->>SW_L1: Loop back to VLAN 204 (Gi0/8)
        SW_L1->>SW_CORE: Loop up to Core SW via VLAN 204
        
        SW_CORE->>HO: Core inspects packet, matches giaddr=204 -> Forwards Request to HO
        HO->>SW_CORE: DHCP ACK (Acknowledge assignment)
        
        Note over SW_CORE, PC: ACK packet loops exactly like Offer 204.y to reach PC
        SW_CORE->>SW_L1: Forward to 1st Floor (VLAN 204)
        SW_L1->>SW_VT: Pass through IT Room SW
        SW_VT->>SW_L1: Loop to VLAN 150
        SW_L1->>SW_CORE: Back to Core SW (VLAN 150)
        SW_CORE->>SW_TRET: Forward to Ground Floor SW
        SW_TRET->>PC: PC officially assigned IP 204.y!
    end
    
    Note over PC, HO: 💡 CISCO RECOMMENDATION (DEFINITIVE SOLUTION):<br/>- Configure Spanning-Tree BPDU Guard on 1st Floor SW (Block looping ports)<br/>- Configure DHCP Snooping (Trust only Uplink ports, drop abnormal DHCP)
```


#### 2. System Administration & High-Performance Computing

* **AI Infrastructure & Cloud GPU Provisioning**
* **Use Case:** Architecting and managing hybrid computing environments for heavy AI/Deep Learning workloads, balancing local resources and cloud scalability.
* **Experience & Solution:** Directly deployed and administered an on-premise AI server infrastructure featuring 4x NVIDIA A5000 GPUs. Implemented **vGPU** virtualization to optimize resource sharing.


* **Enterprise Application Lifecycle & CI/CD Automation**
* **Use Case:** End-to-end development, automation, and release management of enterprise applications with strict security and platform compliance.
* **Experience & Solution:** Built cross-platform UIs using **Flutter** and developed **Python** scripts for system task automation. Designed and maintained **GitLab CI/CD** pipelines to fully automate the build, test, infrastructure setup, and deployment processes, ensuring secure public releases and compliance with the latest Google Play APIs.
