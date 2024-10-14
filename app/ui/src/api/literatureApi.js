// src/api/literatureApi.js
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const searchLiterature = async (query, limit, offset) => {
  try {
    const response = await axios.get(`${BASE_URL}/search/`, {
      params: { query: query, limit: limit, offset: offset },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data from the API", error);
    throw error;
  }
};