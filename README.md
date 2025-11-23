# 🩸 Blood Bank Management System (BBMS) - Frontend Prototype

This repository contains the frontend HTML/CSS prototype for a Blood Bank Management System. The system aims to streamline blood bank operations, facilitate online blood booking, manage donor information, and provide real-time inventory tracking, adhering to national (e.g., Indian) blood bank procedures.

## ✨ Project Overview

The BBMS is designed with three primary user roles:

1.  **Public/Donor:** Individuals interested in donating blood, finding nearby blood banks, or learning more.
2.  **Hospital/Requester:** Authorized hospital staff who need to request blood units for patients.
3.  **Blood Bank Staff/Admin:** Personnel responsible for managing blood inventory, donor records, verifying requests, and generating reports.

This prototype focuses on demonstrating the user interface and basic page structures for these roles.

## 🚀 Features Implemented (Frontend Prototype)

The HTML files cover the core functionalities outlined for the BBMS:

* **Public Portal:**
    * **Home Page (`index.html`):** Project introduction, mission, and calls to action for donation and finding blood banks.
    * **About Us (`about_us.html`):** Information about the organization's vision, mission, and values.
    * **Contact Us (`contact_us.html`):** Contact details and a form for general inquiries, including an embedded map placeholder.
    * **Donor Registration (`donor_register.html`):** Form for new donors to register their personal, contact, and account information.
    * **Donor Login (`donor_login.html`):** Login portal for registered donors.
* **Hospital Portal:**
    * **Hospital Login (`hospital_login.html`):** Secure login for authorized hospital staff.
    * **Hospital Dashboard (`hospital_dashboard.html`):** Overview for hospitals showing pending/approved requests, blood in transit, and quick actions.
* **Admin/Staff Portal:**
    * **Admin Login (`admin_login.html`):** Secure login for blood bank administrators and staff.
    * **Admin Dashboard (`admin_dashboard.html`):** Centralized overview for administrators, showing total units, pending requests, expiry alerts, and recent activities.

## 📁 Project Structure

The project is organized with HTML files representing distinct web pages. For simplicity in this prototype, CSS is embedded directly within each HTML file.

. ├── index.html # Home page (Public/Donor) ├── about_us.html # About Us page (Public/Donor) ├── contact_us.html # Contact Us page (Public/Donor) ├── donor_register.html # Donor registration form (Public/Donor) ├── donor_login.html # Donor login page (Public/Donor) ├── hospital_login.html # Hospital staff login page ├── hospital_dashboard.html # Hospital staff dashboard ├── admin_login.html # Admin/Blood Bank Staff login page ├── admin_dashboard.html # Admin/Blood Bank Staff dashboard ├── (other_pages.html) # Placeholder for future pages like search_bank, request_new, etc. └── README.md # This file


## 📄 Understanding the HTML Files

Each HTML file follows a consistent structure:

* **`<!DOCTYPE html>` & `<html lang="en">`**: Standard HTML5 declaration.
* **`<head>` Section**:
    * `<meta charset="UTF-8">`: Specifies character encoding.
    * `<meta name="viewport"...>`: Ensures responsiveness across devices.
    * `<title>`: Sets the page title shown in the browser tab.
    * `<style>`: **Contains all CSS for that specific page.** In a full project, this would be an external `style.css` file linked via `<link rel="stylesheet" href="style.css">`.
* **`<body>` Section**:
    * **`<header>`**: Contains the main system title and a brief tagline.
    * **`<nav>`**: Global navigation bar with links to various sections/login portals.
    * **`<div class="container">`**: The main content wrapper for the page.
    * **Specific Page Content**: This is where the unique content for each page resides (e.g., forms, text sections, dashboards).
    * **`<footer>`**: Contains copyright information.

### Key Elements & Classes Used:

* `.container`: Main content wrapper for consistent layout.
* `.form-group`: Groups a label and input field in forms.
* `.button-group`: Centers and styles form submission buttons.
* `.dashboard-grid`: (In dashboards) Uses CSS Grid for a responsive card-based layout.
* `.card`: Individual display elements within dashboards.
* `table-responsive`: Wrapper for tables to enable horizontal scrolling on small screens.

## 🔧 How to Run

1.  **Clone this repository** (if it were a real GitHub repo) or **save all the HTML files** into a single folder on your local machine.
2.  Open any of the `.html` files in your web browser (e.g., double-click `index.html`).
3.  Navigate through the pages using the navigation bar.

## 💡 Future Enhancements (Beyond this Prototype)

* **External CSS:** Consolidate all styles into a single, external `style.css` file.
* **JavaScript:**
    * Client-side form validation.
    * Dynamic content loading (e.g., search results for blood banks, real-time inventory updates).
    * Interactive charts for dashboards (e.g., using Chart.js).
* **Backend Integration:** Connect forms and data displays to a server-side language (e.g., Python/Django, Node.js, Java/Spring Boot) and a database (e.g., PostgreSQL, MySQL).
* **User Authentication:** Implement robust session management and user authentication for all secured portals.
* **Accessibility:** Ensure compliance with web accessibility standards.
* **Full Responsiveness:** Enhance CSS for seamless display on all device sizes.
* **Error Handling:** Implement user-friendly error messages and feedback.

---
**Disclaimer:** This is a frontend prototype for demonstration purposes only. It does not include any backend logic, database integration, or robust security features required for a production-ready application.
