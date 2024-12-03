# 各角色擁有的權限

## 一般使用者 (alumni)
* 更新個人資料
    * 格式：
* 查看學位、查看與更新畢業後的職業歷程
    * 格式：
* 查看並報名參加校友會舉辦的活動
    * 格式：
* 查看成就和捐贈
    * 格式：
* 參加校友會：
## 業務經營者 (alumni association)
* 新增 donation 紀錄 (for association)
* 新增活動 (association event)
* 更新幹部名單：
* 校友會成員管理：
## 資料分析師 (data analytics)
* 薪資分析
* 校友捐款分析
* 計算三十重聚的學長姐名單
## 網站管理者 (NTU alumni center)
* 新增 donation 紀錄 (for school)
* 更改權限 (一旦 association 更新幹部名單)
* 各地校友會管理
* 新增、更新或刪除校友的基本資料

ChatGPT:
# DB final project

For the **University Alumni Tracking System**, a wide range of functions will be needed to support the system's features for different user roles (Admin, Alumni, Analysts, and Cadres). Below is a list of potential functions grouped by purpose:

---

### **General Utility Functions**

1. **Authentication and Authorization**
    - `login_user(username, password)`
    - `check_permissions(user_role, action)`
2. **Error Handling**
    - `handle_not_found(entity_name, id)`
    - `validate_input(data, schema)`

---

### **User Management**

1. **Admin Functions**
    - `create_user(username, password, role)`
    - `delete_user(user_id)`
    - `update_user(user_id, data)`
    - `get_user_details(user_id)`
2. **User Role Assignment**
    - `assign_role(user_id, role)`
    - `change_role(user_id, new_role)`

---

### **Alumni Management**

1. **Alumni CRUD**
    - `add_alumni(data)`
    - `get_alumni(alumni_id)`
    - `update_alumni(alumni_id, data)`
    - `delete_alumni(alumni_id)`
2. **Data Queries**
    - `find_alumni_by_name(name)`
    - `get_alumni_by_graduation_year(year)`
    - `list_alumni()`
3. **Alumni-Specific Functions**
    - `update_alumni_career_history(alumni_id, career_data)`
    - `get_alumni_donations(alumni_id)`
    - `get_alumni_achievements(alumni_id)`

---

### **Career History Management**

1. **Career History CRUD**
    - `add_career_history(alumni_id, career_data)`
    - `update_career_history(career_id, data)`
    - `delete_career_history(career_id)`
    - `get_career_history(career_id)`
2. **Career Analysis**
    - `get_salary_trends(department, year_range)`
    - `get_career_paths(alumni_id)`

---

### **Donation Management**

1. **Donation CRUD**
    - `record_donation(alumni_id, donation_data)`
    - `update_donation(donation_id, data)`
    - `delete_donation(donation_id)`
    - `get_donation(donation_id)`
2. **Analysis**
    - `get_total_donations_by_alumni(alumni_id)`
    - `get_top_donors(limit=10)`
    - `get_donation_trends(year_range)`

---

### **Achievement Management**

1. **Achievement CRUD**
    - `add_achievement(alumni_id, achievement_data)`
    - `update_achievement(achievement_id, data)`
    - `delete_achievement(achievement_id)`
    - `get_achievement(achievement_id)`
2. **Queries**
    - `list_achievements(alumni_id)`
    - `find_achievements_by_category(category)`

---

### **Alumni Association Management**

1. **Association CRUD**
    - `create_association(data)`
    - `update_association(association_id, data)`
    - `delete_association(association_id)`
    - `get_association(association_id)`
2. **Membership Management**
    - `add_member_to_association(alumni_id, association_id)`
    - `remove_member_from_association(alumni_id, association_id)`
    - `list_association_members(association_id)`
3. **Event Management**
    - `create_event(association_id, event_data)`
    - `update_event(event_id, data)`
    - `delete_event(event_id)`
    - `list_events_by_association(association_id)`

---

### **Data Analysis Functions (Analysts)**

1. **Trends and Insights**
    - `get_alumni_employment_trends(department, year_range)`
    - `analyze_event_participation_rates()`
    - `calculate_donation_correlations()`
2. **Special Reports**
    - `generate_30_year_reunion_list()`
    - `get_top_achievers(limit=10)`
    - `get_event_participation_statistics(event_id)`

---

### **Event Participation Functions**

1. **Event Participation CRUD**
    - `add_event_participant(alumni_id, event_id)`
    - `remove_event_participant(alumni_id, event_id)`
    - `list_participants(event_id)`
    - `get_participation_by_alumni(alumni_id)`
