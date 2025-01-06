# Influencer Engagement and Sponsorship Coordination Platform

## Project Overview
This platform connects sponsors and influencers for advertising and campaign collaboration. Sponsors can manage ad campaigns, and influencers can benefit financially by participating in campaigns. The system supports three user roles: Admin, Sponsor, and Influencer.

### Features
- **Admin**: Monitors users, campaigns, and ad requests.
- **Sponsor**: Creates and manages campaigns, including budgets and goals.
- **Influencer**: Accepts or rejects ad requests and engages in campaigns.

### Technology Stack
- **Backend**: Flask
- **Frontend**: Jinja2, Bootstrap
- **Database**: SQLite
- **Visualization**: Chart.js

### ER Diagram
The database schema includes the following tables:
1. **User**: Stores user details with role-specific identifiers (`admin`, `sp`, `in`).
2. **Influencer**: Contains influencer-specific details like social media links and niche.
3. **Sponsor**: Includes sponsor details like company and industry.
4. **Campaign**: Tracks campaign details and sponsor associations.
5. **AdRequest**: Manages ad requests, requirements, and statuses.

### Drive Link to Presentation
[Presentation Video](https://drive.google.com/file/d/1wxC2Laa6xM8PNedbqvlyQRA_-xI5JquM/view?usp=sharing)

---

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites
1. Install [Python 3.8+](https://www.python.org/downloads/).
2. Install `pip` for package management.
3. Install [Git](https://git-scm.com/).

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ripu0902/BuZZWorthy.git
   cd BuZZWorthy
    
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows

   pip install -r requirements.txt

   python app.py   
