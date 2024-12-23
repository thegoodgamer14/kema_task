# QR-Code Payment System

This is a **QR-code-based payment system** that allows merchants to create payment links and buyers to process payments by scanning a QR code. The project is divided into two main parts:

1. **Backend**: Built with **Django** and **Django REST Framework (DRF)**, it handles merchant and payment link creation, QR code generation, and payment processing.
2. **Frontend**: Built with **Vue.js**, it provides a user-friendly interface for merchants to create payment links and buyers to process payments.

---

## **Project Overview**

### **Key Features**

1. **Merchant Management**:
   - Create a merchant profile with details like business name, email, and phone.
   - Generate payment links for the merchant.

2. **Payment Link Generation**:
   - Create payment links with details like amount, currency, and description.
   - Generate a QR code for each payment link.

3. **Buyer Payment Processing**:
   - Buyers can scan the QR code to view payment details and process payments.
   - Simulated payment processing without actual payment gateway integration.

4. **Database Management**:
   - PostgreSQL database to store merchant, payment link, and payment data.

---

## **Project Structure**

### **Backend**
- **Framework**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Features**:
  - Merchant and payment link creation.
  - QR code generation.
  - Payment processing.

### **Frontend**
- **Framework**: Vue.js
- **Features**:
  - Merchant and payment link creation interface.
  - QR code display.
  - Buyer payment processing interface.

---

### **Google Drive Folder**
- [Contains Video Demonstration of the Project and ER Diagram](https://drive.google.com/drive/folders/1E0pEPLoaxEgjxrV5cEs9GyUaeVzPS-RK?usp=sharing)

---

If the backend and frontend are part of the same repository, the setup instructions can be simplified. Here's how you can update the README to reflect this:

---

### **Setup Instructions**

#### **1. Clone the Repository**
```bash
git clone https://github.com/thegoodgamer14/kema_task.git
```

#### **2. Backend Setup**
1. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the database and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Run the backend development server:
   ```bash
   ./runserver.bat
   ```

#### **3. Frontend Setup**
1. Navigate to the frontend directory:
   ```bash
   cd ../kema_payment_task_frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Run the frontend development server:
   ```bash
   npm run serve
   ```

---

### **Testing the Application**

1. **Backend**:
   - Ensure the backend server is running at `http://localhost:8008`.

2. **Frontend**:
   - Ensure the frontend server is running at `http://localhost:8080`.

3. **Merchant Page**:
   - Navigate to `http://localhost:8080/merchant`.
   - Create a merchant and a payment link.
   - Verify that the QR code is generated and the "Go to Buyer Page" button is displayed.

4. **Buyer Page**:
   - Click the "Go to Buyer Page" button or scan the QR code.
   - Verify that the payment details (amount, currency, description) are displayed.
   - Process a payment by submitting buyer details.

`Note: Since the project is not yet deployed, the QR code is generated along with an embedded button that redirects the buyers directly to the payment page, where they can complete the payment process. However, the QR code still contains the embedded link to the payments page (although it cannot be directly accessed on mobile devices since it is still a localhost based link).`
