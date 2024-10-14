// src/api/literatureApi.js
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const searchLiterature = async (query, limit, offset) => {
  const params = {};
  if (query) params.query = query;
  if (limit) params.limit = limit;
  if (offset) params.offset = offset;
  try {
    const response = await axios.get(`${BASE_URL}/search/`, {
      params: params,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data from the API", error);
    throw error;
  }
};