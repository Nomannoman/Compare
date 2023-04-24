import Axios from 'axios';

export var DefaultURL = window.location.origin;

DefaultURL = DefaultURL.slice(0,-1)+'4';
const options={
    baseURL : DefaultURL,
    headers:{
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
    }
}

export const apicaller = Axios.create(options);