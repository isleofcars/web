import axios from 'axios';

const DEFAULT_API_URL = 'https://wholecarsmarket.com/';

class Api {
    constructor() {
        this.apiClient = axios.create({
            baseURL: process.env.VUE_APP_API_URL || DEFAULT_API_URL,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        });

        this.getCarsRequest = axios.CancelToken.source();
    }

    getCars(page = 1, filtersQuery = '') {
        this.getCarsRequest = axios.CancelToken.source();
        return this.apiClient.get(`/api/v1/cars?page=${page}&${filtersQuery}`, {
            cancelToken: this.getCarsRequest.token,
        });
    }

    getMinYear() {
        return this.apiClient.get('/api/v1/min_year');
    }

    getUserCity() {
        return this.apiClient.get('/api/v1/usercity');
    }

    getMakes() {
        return this.apiClient.get('/api/v1/makes');
    }

    cancelRequest() {
        if (this.getCarsRequest !== null) {
            try {
                this.getCarsRequest.cancel();
            } catch (e) {
                console.log(e);
            }
        }
    }
}

export const getPlacesForZIP = (zipCode) => axios.get(`https://api.zippopotam.us/us/${zipCode}`, {
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
});

export const API = new Api();
