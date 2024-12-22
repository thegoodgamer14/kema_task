<template>
    <div class="merchant-page">
      <h1>Merchant Page</h1>
  
      <!-- Merchant Form -->
      <form @submit.prevent="createMerchant">
        <div>
          <label for="business_name">Business Name:</label>
          <input type="text" id="business_name" v-model="merchantForm.business_name" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="merchantForm.email" required />
        </div>
        <div>
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="merchantForm.phone" required />
        </div>
        <button type="submit">Create Merchant</button>
      </form>
  
      <!-- Payment Link Form -->
      <form @submit.prevent="createPaymentLink">
        <div>
          <label for="amount">Amount:</label>
          <input type="number" id="amount" v-model="paymentLinkForm.amount" required />
        </div>
        <div>
          <label for="currency">Currency:</label>
          <input type="text" id="currency" v-model="paymentLinkForm.currency" required />
        </div>
        <div>
          <label for="description">Description:</label>
          <input type="text" id="description" v-model="paymentLinkForm.description" required />
        </div>
        <button type="submit">Create Payment Link</button>
      </form>
  
      <!-- QR Code Display -->
      <div v-if="qrCodeImage">
        <h2>Scan the QR Code to Pay</h2>
        <img :src="qrCodeImage" alt="QR Code" />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import QRCode from 'qrcode';
  
  export default {
    data() {
      return {
        merchantForm: {
          business_name: '',
          email: '',
          phone: ''
        },
        paymentLinkForm: {
          amount: '',
          currency: '',
          description: ''
        },
        qrCodeImage: ''
      };
    },
    methods: {
      async createMerchant() {
        try {
          const response = await axios.post('http://localhost:8008/api/merchants/', this.merchantForm);
          console.log('Merchant created:', response.data);
          alert('Merchant created successfully!');
        } catch (error) {
          console.error('Error creating merchant:', error);
          alert('Failed to create merchant. Please try again.');
        }
      },
      async createPaymentLink() {
        try {
          const response = await axios.post('http://localhost:8008/api/payment-links/', {
            merchant: this.merchantId,
            amount: this.paymentLinkForm.amount,
            currency: this.paymentLinkForm.currency,
            description: this.paymentLinkForm.description
          });
          console.log('Payment link created:', response.data);

          // Generate the QR code with the buyer page URL
          const buyerPageUrl = `http://localhost:8080/buyer/${response.data.id}`; // Replace with your frontend URL
          this.qrCodeImage = await QRCode.toDataURL(buyerPageUrl);

          alert('Payment link created successfully!');
        } catch (error) {
          console.error('Error creating payment link:', error);
          alert('Failed to create payment link. Please try again.');
        }
      },
    }
  };
  </script>
  
  <style scoped>
  .merchant-page {
    padding: 20px;
  }
  form {
    margin-bottom: 20px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
  </style>