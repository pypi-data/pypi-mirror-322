/**
 * SCRIPT was pulled from Python Stress Tests
 * https://verses.atlassian.net/wiki/spaces/QA/pages/1183973380/Python+Stress+Test+Fun
 * 
 * Usage Example:
 * TARGET_URL=http://localhost:3000 K6_VUS=10 K6_DURATION=1m k6 run k6_batchtest.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration from environment variables
const targetUrl = __ENV.TARGET_URL || 'https://gpil-server-qa-e2e-test.genius-agent-stable.dev.verses.build/';
const vus = parseInt(__ENV.K6_VUS || '10'); // Number of virtual users
const duration = __ENV.K6_DURATION || '30m'; // Test duration

// Define K6 options
export const options = {
  vus: vus,
  duration: duration,
};

// Endpoints with methods and payloads
const requests = [
  {
    description: 'GET /',
    method: 'GET',
    endpoint: '/',
    headers: { accept: 'application/json' },
  },
  {
    description: 'GET /graph',
    method: 'GET',
    endpoint: '/graph',
    headers: { accept: 'application/json' },
  },
  {
    description: 'POST /graph',
    method: 'POST',
    endpoint: '/graph',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      vfg: {
        factors: [
          { distribution: 'categorical', values: [0.5, 0.5], variables: ['cloudy'] },
          {
            distribution: 'categorical_conditional',
            values: [[0.8, 0.2], [0.2, 0.8]],
            variables: ['rain', 'cloudy'],
          },
        ],
        variables: {
          cloudy: { elements: ['no', 'yes'] },
          rain: { elements: ['no', 'yes'] },
        },
        version: '0.3.0',
      },
    }),
  },
  {
    description: 'POST /infer',
    method: 'POST',
    endpoint: '/infer',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      library: 'pgmpy',
      variable_id: 'sprinkler',
      evidence: { cloudy: 'yes' },
    }),
  },
  {
    description: 'POST /actionselection',
    method: 'POST',
    endpoint: '/actionselection',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      library: 'pymdp',
      observation: 2,
      policy_len: 3,
    }),
  },
  {
    description: 'POST /learn',
    method: 'POST',
    endpoint: '/learn',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      observations_csv: 'cloudy,rain,sprinkler,wet_grass\nyes,yes,on,yes\nno,no,off,no',
      library: 'pgmpy',
    }),
  },
  {
    description: 'POST /import',
    method: 'POST',
    endpoint: '/import',
    headers: { 'Content-Type': 'application/csv' },
    payload: `OrderID,CustomerID,EmployeeID,OrderDate,ShipperID,ProductID,Quantity,ProductName,Price,CompanyName
10248,90,5,1996-07-04,3,11,12,Queso Cabrales,21,Wilman Kala
10249,81,6,1996-07-05,1,14,9,Tofu,23.25,Tradição Hipermercados`,
  },
  {
    description: 'POST /validate',
    method: 'POST',
    endpoint: '/validate',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      vfg: {
        factors: [
          { distribution: 'categorical', values: [0.5, 0.5], variables: ['cloudy'] },
          {
            distribution: 'categorical_conditional',
            values: [[0.8, 0.2], [0.2, 0.8]],
            variables: ['rain', 'cloudy'],
          },
        ],
        variables: {
          cloudy: { elements: ['no', 'yes'] },
          rain: { elements: ['no', 'yes'] },
        },
        version: '0.3.0',
      },
    }),
  },
];

// Main K6 execution function
export default function () {
  // Build the batch requests
  const batchRequests = requests.map((req) => {
    const url = `${targetUrl}${req.endpoint}`;
    return req.method === 'GET'
      ? { method: 'GET', url: url, params: { headers: req.headers } }
      : { method: 'POST', url: url, body: req.payload, params: { headers: req.headers } };
  });

  // Send all requests in parallel using http.batch
  const responses = http.batch(batchRequests);

  // Check and log results for each request
  responses.forEach((response, index) => {
    const req = requests[index];
    const success = check(response, {
      [`${req.description} - status is 200`]: (r) => r.status === 200,
    });

    if (!success) {
      console.warn(
        `${req.description} failed with status ${response.status}, Response body: ${response.body}`
      );
    }

    console.log(
      `${req.description}: Status ${response.status}, Response Time: ${response.timings.duration} ms`
    );
  });

  sleep(1); // Brief sleep to simulate pacing
}