import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    duration: '1m',  // Increase the duration of the test
    vus: 1000,         // Increase the number of virtual users
  };

export default function () {
    http.get(`http://${__ENV.TARGET_HTTP_HOSTNAME}:${__ENV.TARGET_HTTP_PORT}/users`);
    sleep(1);
}