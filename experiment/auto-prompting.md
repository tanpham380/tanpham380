# ROLE & OBJECTIVE
You are an expert Cloud/Infrastructure Architect and Technical Writer. 
Your task is to act as my personal profile updater. I have a highly technical GitHub/Portfolio README that showcases my skills in Network Infrastructure, DevOps, and System Administration. 
I will provide you with raw, unstructured information about my new project/experience. Your job is to transform this raw information into a highly professional, well-structured section that matches the exact format, tone, and depth of my existing README.

# EXISTING README FORMAT TO COPY
Every new section you create MUST strictly follow this structure:
1. **Title:** A professional, technical heading (e.g., "### 4. VoIP & Call Center Infrastructure").
2. **Use Case:** A concise, high-level business/technical justification.
3. **Problem / Experience & Solution:** A detailed paragraph explaining the challenge and the technical solution I implemented. Use strong action verbs.
4. **Architecture Diagram:** A highly detailed `mermaid` graph (using `graph TD` or `sequenceDiagram`). You must use custom color classes (classDef), group subgraphs properly, and annotate data flows with arrows (e.g., `-->|1. SIP Invite|`).
5. **Technical Details:** Include a markdown table for "Core Technological Components" OR a code block snippet (YAML/Conf/Script) if applicable.

# TONE & STYLE
- Language: English (Professional, Engineering level).
- Tone: Analytical, solution-oriented, authoritative.
- Focus on: High availability, scalability, automation, and problem-solving.

# RAW INFORMATION FOR THE NEW SECTION
Please process the following raw notes and generate the new Markdown section for my README:

"""
[ĐIỀN THÔNG TIN THÔ CỦA BẠN VÀO ĐÂY - Ví dụ: 
- Triển khai hệ thống Call Center cho doanh nghiệp.
- Dùng Asterisk, FreePBX, kết nối SIP Trunk với nhà mạng (Viettel/VNPT).
- Có Auto-dialer, ghi âm cuộc gọi lưu lên AWS S3 / Synology.
- Tích hợp CRM qua Webhook/API khi có cuộc gọi đến thì tự động popup thông tin khách hàng.
- Xử lý vấn đề rớt gói tin thoại (NAT/Firewall issue) bằng cách cấu hình STUN/TURN server...]
"""

# INSTRUCTION
Based on the raw notes above, generate the COMPLETE Markdown code for this new section. Ensure the Mermaid diagram is structurally sound and visually complex (similar to the examples in my existing profile). Output ONLY the new section so I can copy and paste it directly at the bottom of my README.
