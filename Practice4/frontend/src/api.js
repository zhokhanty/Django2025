import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/items/';

export const getItems = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Error fetching items:", error);
        return [];
    }
};

export const createItem = async (item) => {
    try {
        const response = await axios.post(API_URL, item);
        return response.data;
    } catch (error) {
        console.error("Error creating item:", error);
        return null;
    }
};
