import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const getUserQueries = async () => {
  const response = await axios.get(`${BASE_URL}/metrics/user-queries/`);
  return response.data;
};

export const getOpenAIMetrics = async () => {
  const response = await axios.get(`${BASE_URL}/metrics/openai-performance/`);
  return response.data;
};