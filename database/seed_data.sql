-- ============================================================
-- seed_data.sql  -  Sample Opportunities Data (40+ records)
-- University of Central Punjab  |  Tools & Techniques for DS
-- ============================================================

INSERT INTO opportunities
    (company_name, job_title, category, city, country, work_mode,
     required_skills, salary_min, salary_max, currency,
     experience_level, application_deadline, status, source_link)
VALUES

-- ── Systems Limited ─────────────────────────────────────────
('Systems Limited', 'Data Science Intern', 'Data Science', 'Lahore', 'Pakistan', 'Onsite',
 'Python, pandas, scikit-learn, SQL', 40000, 60000, 'PKR', 'Entry Level', '2026-07-15', 'Open',
 'https://www.systemsltd.com/careers'),

('Systems Limited', 'Machine Learning Engineer', 'Data Science', 'Karachi', 'Pakistan', 'Hybrid',
 'Python, TensorFlow, PyTorch, MLOps, Docker', 150000, 220000, 'PKR', 'Mid Level', '2026-07-30', 'Open',
 'https://www.systemsltd.com/careers'),

('Systems Limited', 'Junior Web Developer', 'Web Development', 'Lahore', 'Pakistan', 'Onsite',
 'React, Node.js, REST APIs, Git', 60000, 90000, 'PKR', 'Entry Level', '2026-06-20', 'Closed',
 'https://www.systemsltd.com/careers'),

('Systems Limited', 'Cyber Security Analyst', 'Cyber Security', 'Islamabad', 'Pakistan', 'Onsite',
 'SIEM, Penetration Testing, Wireshark, Python', 120000, 180000, 'PKR', 'Mid Level', '2026-06-10', 'Expired',
 'https://www.systemsltd.com/careers'),

('Systems Limited', 'AI Research Intern', 'AI', 'Lahore', 'Pakistan', 'Hybrid',
 'Python, NLP, Transformers, HuggingFace', 50000, 70000, 'PKR', 'Entry Level', '2026-08-01', 'Open',
 'https://www.systemsltd.com/careers'),

-- ── Netsol Technologies ──────────────────────────────────────
('Netsol Technologies', 'Software Engineer – AI', 'AI', 'Lahore', 'Pakistan', 'Hybrid',
 'Python, LLMs, FastAPI, PostgreSQL', 180000, 260000, 'PKR', 'Mid Level', '2026-07-20', 'Open',
 'https://www.netsoltech.com/careers'),

('Netsol Technologies', 'Full Stack Developer', 'Web Development', 'Lahore', 'Pakistan', 'Onsite',
 'Vue.js, Django, PostgreSQL, Docker', 100000, 160000, 'PKR', 'Mid Level', '2026-08-10', 'Open',
 'https://www.netsoltech.com/careers'),

('Netsol Technologies', 'Data Analyst Intern', 'Data Science', 'Lahore', 'Pakistan', 'Remote',
 'SQL, Excel, Power BI, Python', 35000, 50000, 'PKR', 'Entry Level', '2026-07-05', 'Shortlisted',
 'https://www.netsoltech.com/careers'),

('Netsol Technologies', 'SOC Engineer', 'Cyber Security', 'Karachi', 'Pakistan', 'Onsite',
 'Splunk, Firewall, IDS/IPS, Linux', 130000, 190000, 'PKR', 'Mid Level', '2026-06-25', 'Closed',
 'https://www.netsoltech.com/careers'),

('Netsol Technologies', 'Senior Data Scientist', 'Data Science', 'Lahore', 'Pakistan', 'Hybrid',
 'Python, Spark, ML, Statistics, Azure ML', 280000, 380000, 'PKR', 'Senior Level', '2026-08-20', 'Open',
 'https://www.netsoltech.com/careers'),

-- ── Arbisoft ─────────────────────────────────────────────────
('Arbisoft', 'AI Engineer', 'AI', 'Lahore', 'Pakistan', 'Remote',
 'Python, LangChain, OpenAI API, Vector DBs', 200000, 300000, 'PKR', 'Mid Level', '2026-07-25', 'Open',
 'https://arbisoft.com/careers'),

('Arbisoft', 'Backend Developer', 'Software Engineering', 'Lahore', 'Pakistan', 'Hybrid',
 'Python, Django, REST, Celery, Redis', 120000, 180000, 'PKR', 'Mid Level', '2026-07-18', 'Open',
 'https://arbisoft.com/careers'),

('Arbisoft', 'Data Science Intern', 'Data Science', 'Lahore', 'Pakistan', 'Onsite',
 'Python, NumPy, pandas, Matplotlib', 40000, 55000, 'PKR', 'Entry Level', '2026-06-30', 'Expired',
 'https://arbisoft.com/careers'),

('Arbisoft', 'DevOps Engineer', 'Software Engineering', 'Lahore', 'Pakistan', 'Remote',
 'AWS, Docker, Kubernetes, Terraform, CI/CD', 200000, 300000, 'PKR', 'Senior Level', '2026-08-15', 'Open',
 'https://arbisoft.com/careers'),

('Arbisoft', 'Penetration Tester', 'Cyber Security', 'Islamabad', 'Pakistan', 'Hybrid',
 'Kali Linux, Burp Suite, Metasploit, OWASP', 160000, 230000, 'PKR', 'Mid Level', '2026-07-10', 'Shortlisted',
 'https://arbisoft.com/careers'),

('Arbisoft', 'React Native Developer', 'Web Development', 'Lahore', 'Pakistan', 'Remote',
 'React Native, TypeScript, Redux, REST APIs', 140000, 200000, 'PKR', 'Mid Level', '2026-08-05', 'Open',
 'https://arbisoft.com/careers'),

-- ── 10Pearls ─────────────────────────────────────────────────
('10Pearls', 'Junior Data Scientist', 'Data Science', 'Karachi', 'Pakistan', 'Onsite',
 'Python, scikit-learn, SQL, Tableau', 80000, 120000, 'PKR', 'Entry Level', '2026-07-22', 'Open',
 'https://10pearls.com/careers'),

('10Pearls', 'NLP Engineer', 'AI', 'Karachi', 'Pakistan', 'Remote',
 'Python, spaCy, HuggingFace, BERT, FastAPI', 220000, 320000, 'PKR', 'Senior Level', '2026-08-12', 'Open',
 'https://10pearls.com/careers'),

('10Pearls', 'Cloud Security Engineer', 'Cyber Security', 'Karachi', 'Pakistan', 'Hybrid',
 'AWS Security, IAM, GuardDuty, CloudTrail', 200000, 280000, 'PKR', 'Mid Level', '2026-07-28', 'Open',
 'https://10pearls.com/careers'),

('10Pearls', 'Frontend Developer', 'Web Development', 'Karachi', 'Pakistan', 'Onsite',
 'React, TypeScript, Tailwind CSS, GraphQL', 100000, 150000, 'PKR', 'Mid Level', '2026-06-28', 'Closed',
 'https://10pearls.com/careers'),

('10Pearls', 'ML Ops Engineer', 'Data Science', 'Karachi', 'Pakistan', 'Remote',
 'MLflow, Docker, Kubernetes, Python, AWS', 250000, 350000, 'PKR', 'Senior Level', '2026-08-20', 'Open',
 'https://10pearls.com/careers'),

('10Pearls', 'Software Engineer Intern', 'Software Engineering', 'Karachi', 'Pakistan', 'Onsite',
 'Java, Spring Boot, Git, MySQL', 35000, 50000, 'PKR', 'Entry Level', '2026-07-01', 'Shortlisted',
 'https://10pearls.com/careers'),

-- ── Folio3 ────────────────────────────────────────────────────
('Folio3', 'Computer Vision Engineer', 'AI', 'Islamabad', 'Pakistan', 'Hybrid',
 'Python, OpenCV, YOLO, TensorFlow, PyTorch', 200000, 280000, 'PKR', 'Mid Level', '2026-07-15', 'Open',
 'https://www.folio3.com/careers'),

('Folio3', 'Data Engineer', 'Data Science', 'Islamabad', 'Pakistan', 'Remote',
 'Apache Spark, Airflow, Python, PostgreSQL, AWS', 220000, 320000, 'PKR', 'Mid Level', '2026-08-08', 'Open',
 'https://www.folio3.com/careers'),

('Folio3', 'Security Analyst Intern', 'Cyber Security', 'Islamabad', 'Pakistan', 'Onsite',
 'Network Security, Vulnerability Assessment, Linux', 30000, 45000, 'PKR', 'Entry Level', '2026-07-10', 'Open',
 'https://www.folio3.com/careers'),

('Folio3', 'Node.js Developer', 'Web Development', 'Islamabad', 'Pakistan', 'Onsite',
 'Node.js, Express, MongoDB, REST API', 100000, 160000, 'PKR', 'Mid Level', '2026-06-15', 'Expired',
 'https://www.folio3.com/careers'),

('Folio3', 'QA Engineer', 'Software Engineering', 'Islamabad', 'Pakistan', 'Hybrid',
 'Selenium, Python, JIRA, Manual Testing', 80000, 120000, 'PKR', 'Entry Level', '2026-08-01', 'Open',
 'https://www.folio3.com/careers'),

('Folio3', 'Senior AI/ML Researcher', 'AI', 'Islamabad', 'Pakistan', 'Remote',
 'Research, Deep Learning, GANs, Reinforcement Learning', 350000, 500000, 'PKR', 'Senior Level', '2026-09-01', 'Open',
 'https://www.folio3.com/careers'),

-- ── Remotebase (Remote-First) ──────────────────────────────────
('Remotebase', 'Python Developer', 'Software Engineering', 'Lahore', 'Pakistan', 'Remote',
 'Python, FastAPI, PostgreSQL, Docker, AWS', 150000, 250000, 'PKR', 'Mid Level', '2026-07-20', 'Open',
 'https://remotebase.com/jobs'),

('Remotebase', 'Data Science Consultant', 'Data Science', 'Peshawar', 'Pakistan', 'Remote',
 'Python, ML, Statistics, Communication, Jupyter', 200000, 300000, 'PKR', 'Senior Level', '2026-08-10', 'Open',
 'https://remotebase.com/jobs'),

('Remotebase', 'AI Product Manager', 'AI', 'Peshawar', 'Pakistan', 'Remote',
 'Product Management, AI Concepts, Jira, Roadmapping', 300000, 450000, 'PKR', 'Senior Level', '2026-07-30', 'Open',
 'https://remotebase.com/jobs'),

('Remotebase', 'Blockchain Developer', 'Software Engineering', 'Karachi', 'Pakistan', 'Remote',
 'Solidity, Web3.js, Ethereum, Smart Contracts', 200000, 350000, 'PKR', 'Mid Level', '2026-06-18', 'Closed',
 'https://remotebase.com/jobs'),

('Remotebase', 'Ethical Hacker', 'Cyber Security', 'Peshawar', 'Pakistan', 'Remote',
 'CEH, OSCP, Python, Networking, OWASP Top 10', 220000, 350000, 'PKR', 'Senior Level', '2026-08-25', 'Open',
 'https://remotebase.com/jobs'),

('Remotebase', 'Full Stack Engineer', 'Web Development', 'Peshawar', 'Pakistan', 'Remote',
 'Next.js, Python, PostgreSQL, Redis, AWS', 180000, 270000, 'PKR', 'Mid Level', '2026-07-15', 'Shortlisted',
 'https://remotebase.com/jobs'),

-- ── Extra mixed records to exceed 40 ─────────────────────────
('Systems Limited', 'NLP Research Intern', 'AI', 'Lahore', 'Pakistan', 'Hybrid',
 'Python, NLP, TF-IDF, Transformers', 45000, 65000, 'PKR', 'Entry Level', '2026-06-17', 'Open',
 'https://www.systemsltd.com/careers'),

('Netsol Technologies', 'Cloud Solutions Architect', 'Software Engineering', 'Islamabad', 'Pakistan', 'Hybrid',
 'AWS, Azure, Terraform, Kubernetes, Python', 350000, 500000, 'PKR', 'Senior Level', '2026-08-30', 'Open',
 'https://www.netsoltech.com/careers'),

('Arbisoft', 'Business Intelligence Analyst', 'Data Science', 'Lahore', 'Pakistan', 'Onsite',
 'Power BI, SQL, Excel, DAX, ETL', 90000, 140000, 'PKR', 'Mid Level', '2026-07-05', 'Open',
 'https://arbisoft.com/careers'),

('10Pearls', 'Android Developer', 'Software Engineering', 'Karachi', 'Pakistan', 'Onsite',
 'Kotlin, Android SDK, REST, Firebase', 110000, 170000, 'PKR', 'Mid Level', '2026-07-12', 'Open',
 'https://10pearls.com/careers'),

('Folio3', 'IoT Software Engineer', 'Software Engineering', 'Islamabad', 'Pakistan', 'Hybrid',
 'C++, Python, MQTT, Embedded Linux, AWS IoT', 160000, 240000, 'PKR', 'Mid Level', '2026-08-18', 'Open',
 'https://www.folio3.com/careers'),

('Remotebase', 'Generative AI Engineer', 'AI', 'Lahore', 'Pakistan', 'Remote',
 'LangChain, LlamaIndex, OpenAI, Pinecone, Python', 280000, 420000, 'PKR', 'Senior Level', '2026-09-05', 'Open',
 'https://remotebase.com/jobs');
