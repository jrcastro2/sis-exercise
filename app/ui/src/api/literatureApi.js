// src/api/literatureApi.js
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api';  // Adjust this based on your Django backend URL

export const searchLiterature = async (query, limit) => {
  try {
    const response = await axios.get(`${BASE_URL}/search/`, {
      params: { query: query, limit: limit },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data from the API", error);
    throw error;
  }
};