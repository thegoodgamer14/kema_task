<template>
    <div class="buyer-page">
      <h1>Buyer Page</h1>
  
      <!-- Payment Details -->
      <div v-if="paymentLink">
        <p><strong>Amount:</strong> {{ paymentLink.amount }}</p>
        <p><strong>Currency:</strong> {{ paymentLink.currency }}</p>
        <p><strong>Description:</strong> {{ paymentLink.description }}</p>
      </div>
  
      <!-- Payment Form -->
      <form @submit.prevent="processPayment">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="buyerDetails.name" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="buyerDetails.email" required />
        </div>
        <div>
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="buyerDetails.phone" required />
        </div>
        <button type="submit">Pay Now</button>
      </form>
  
      <!-- Payment Status -->
      <div v-if="paymentStatus">
        <h2>{{ paymentStatus }}</h2>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        paymentLinkId: this.$route.params.paymentLinkId,
        paymentLink: null,
        buyerDetails: {
          name: '',
          email: '',
          phone: ''
        },
        paymentStatus: ''
      };
    },
    async created() {
      await this.fetchPaymentLink();
    },
    methods: {
      async fetchPaymentLink() {
        try {
          const response = await axios.get(`http://localhost:8008/api/payment-links/${this.paymentLinkId}/check_status/`);
          this.paymentLink = response.data;
        } catch (error) {
          console.error('Error fetching payment link:', error);
          alert('Failed to fetch payment details. Please try again.');
        }
      },
      async processPayment() {
        try {
          const response = await axios.post('http://localhost:8008/api/payments/process_payment/', {
            payment_link_id: this.paymentLinkId,
            buyer: this.buyerDetails
          });
          console.log('Payment processed:', response.data);
          this.paymentStatus = response.data.message;
          alert('Payment processed successfully!');
        } catch (error) {
          console.error('Error processing payment:', error);
          alert('Failed to process payment. Please try again.');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .buyer-page {
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
    background-color: #28a745;
    color: white;
    border: none;
    cursor: pointer;
  }
  button:hover {
    background-color: #218838;
  }
  </style>