import http from "k6/http";
import { check } from "k6";
export let options = {
  vus: 1,
  duration: "10s",
};

export default function () {
  const url = "http://localhost/status";
  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const user_id = gen(5);
  const payload = JSON.stringify({
    id: user_id,
  });

  let res = http.post(url, payload, params);
  check(res, { "status was 200": (r) => r.status == 200 });

  res = http.get(`http://localhost/status/${user_id}`);
  check(res, { "status was 200": (r) => r.status == 200 });
}

function gen(length) {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  let result = "";
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
