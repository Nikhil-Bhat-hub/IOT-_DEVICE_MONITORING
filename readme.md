 **IoT Device Monitoring \& KPI Analytics Platform**



An AI-powered IoT device monitoring system that tracks device performance, visualizes KPIs, and detects anomalies using Machine Learning.



Built using Python, Streamlit, MySQL, Plotly, and Scikit-learn.







**Project Overview**



This project simulates a real-world IoT monitoring platform similar to enterprise solutions used in telecom and device management industries.



The system allows:



\- Monitoring connected devices

\- Tracking operational KPIs

\- Visualizing performance metrics

\- Detecting anomalies using AI







 **Tech Stack**



\- Backend: Python

\- Database: MySQL

\- Dashboard: Streamlit

\- Visualization: Plotly

\- Machine Learning: Scikit-learn (Isolation Forest)

\- Data Processing: Pandas, NumPy



---



**Key Features**



&nbsp;Device Management

\- Add new IoT devices

\- Track device location, signal strength, and data usage

\- Monitor device status (Active / Inactive / Faulty)



KPI Dashboard

\- Total Devices

\- Active Devices

\- Faulty Devices

\- Data Usage Trends

\- Status Distribution Pie Chart



AI Anomaly Detection

\- Uses Isolation Forest algorithm

\- Detects abnormal signal strength and data usage

\- Visualizes anomalies using interactive charts







**Database Schema**



Devices Table



| Column | Type |

|--------|------|

| device\_id | VARCHAR |

| device\_name | VARCHAR |

| location | VARCHAR |

| status | VARCHAR |

| signal\_strength | INT |

| data\_usage\_mb | FLOAT |

| last\_active | DATETIME |










