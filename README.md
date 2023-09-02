# Employee Survey System

---
##### **system actors:**

- **Admin**
- **Employee (Name - JobTitle - department  ) ( Allow self-register)**


---
##### **The system has three data objects:**
- Question
- Answers
- Survey --> list of rating questions - has three types (general, followers, reversed) - has start date - has an end date

---
##### views (implemented as a restful API and template view):---
1.  **Employee tree view**  -> *set up by the admin*     Every employee can have a parent employee that they report to as the above fig
    ![Untitled Diagram drawio (1)](https://user-images.githubusercontent.com/30774866/187946789-b02f8be0-4a84-424b-89bd-6b33170aaa99.png)

2. **survey view**

    1. view for due surveys [list]
    2. View for submitted surveys [list]
    3. View for fetching a single survey question [detail]
    4. view for submitting the answer for the survey  [POST - Form]
    5. Employee real-time chatting system using WebSockets
---
##### **Admin flow**

1.  Admin only can create (question, surveys)
2.  Admin can lunch survey for three different channel
    - general --> means that all the system users besides the Admins will get that survey
    - followers --> mean that all the parents will get a survey on every child in their tree (for example a senior software engineer reviewing his team juniors engineer  )
    - reversed --> means all the children will receive a survey on the parent employee
---
