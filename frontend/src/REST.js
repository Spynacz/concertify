import AWS from "aws-sdk";

export function cartPost(token, cart) {
  const newCart = cart.map(({ quantity, amount, ticket_type, ...rest }) => {
    return { quantity, amount, ticket_type };
  });
  const json = JSON.stringify({ items: newCart });
  fetch("http://localhost:8000/cart", {
    method: "POST",
    body: json,
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      Authorization: "Token " + token,
    },
  }).then((response) => {
    if (!response.ok) throw response;
  });
}

export function cartGet(token) {
  return fetch("http://localhost:8000/cart", {
    method: "GET",
    headers: {
      Authorization: "Token " + token,
    },
  })
    .then((response) => {
      if (!response.ok) throw response;
      return response.json();
    })
    .then((data) => {
      return data.items;
    })
    .catch((err) => {
      if (err.status === 400) {
        return [];
      } else {
        throw err;
      }
    });
}

export function eventGet(id) {
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return fetch(`http://localhost:8000/event/${id}`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) throw response;
      return response.json();
    })
    .then((data) => {
      return {
        ...data,
        start: new Date(data.start).toLocaleDateString(undefined, options),
        end: new Date(data.end).toLocaleDateString(undefined, options),
      };
    });
}

export function eventList() {
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return fetch("http://localhost:8000/event", {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) throw response;
      return response.json();
    })
    .then((data) => {
      return data.results.map((event) => ({
        ...event,
        start: new Date(event.start).toLocaleDateString(undefined, options),
      }));
    });
}

export function logoutPost(token) {
  return fetch("http://localhost:8000/logout", {
    method: "POST",
    headers: {
      Authorization: "Token " + token,
    },
  });
}

export function loginPost(username, password) {
  return fetch("http://localhost:8000/login", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
    headers: { "Content-type": "application/json; charset=UTF-8" },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function registerPost(username, password, email, first_name, last_name) {
  return fetch("http://localhost:8000/create", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      email: email,
      first_name: first_name,
      last_name: last_name,
      password: password,
      payment_info: {},
    }),
    headers: { "Content-type": "application/json; charset=UTF-8" },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function profileGet(token) {
  return fetch("http://localhost:8000/profile", {
    method: "GET",
    headers: {
      Authorization: "Token " + token,
    },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function profilePatch(token, username, email, first_name, last_name) {
  return fetch("http://localhost:8000/profile", {
    method: "PATCH",
    body: JSON.stringify({
      username: username,
      email: email,
      first_name: first_name,
      last_name: last_name,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      Authorization: "Token " + token,
    },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function profilePatchPayment(
  token,
  line1,
  line2,
  city,
  postal_code,
  country,
  telephone,
  mobile,
) {
  return fetch("http://localhost:8000/profile", {
    method: "PATCH",
    body: JSON.stringify({
      payment_info: {
        line1: line1,
        line2: line2,
        city: city,
        postal_code: postal_code,
        country: country,
        telephone: telephone,
        mobile: mobile,
      },
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      Authorization: "Token " + token,
    },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function profileDelete(token) {
  return fetch("http://localhost:8000/profile", {
    method: "DELETE",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      Authorization: "Token " + token,
    },
  });
}

export function profilePut(token, old_pass, pass1, pass2) {
  return fetch("http://localhost:8000/profile/password", {
    method: "PUT",
    body: JSON.stringify({
      old_password: old_pass,
      password1: pass1,
      password2: pass2,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
      Authorization: "Token " + token,
    },
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}

export function uploadImageToS3(file) {
  const S3_BUCKET = process.env.S3_BUCKET;
  const REGION = process.env.S3_REGION;

  AWS.config.update({
    accessKeyId: process.env.S3_ACCESS_KEY,
    secretAccessKey: process.env.S3_SECRET_KEY,
    region: REGION,
  });

  const myBucket = new AWS.S3({
    params: { Bucket: S3_BUCKET },
    region: REGION,
  });

  const uploadFile = () => {
    const params = {
      Body: file,
      Bucket: S3_BUCKET,
      Key: file.name,
      ContentType: file.type,
    };

    return myBucket
      .putObject(params)
      .promise()
      .then(() => {
        const location = `https://${S3_BUCKET}.s3.${REGION}.amazonaws.com/${file.name}`;
        return location;
      })
      .catch((err) => {
        throw err;
      });
  };

  return uploadFile();
}

export function postPost(token, title, desc, picture, event) {
  return fetch("http://localhost:8000/post", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Authorization: "Token " + token,
    },
    body: JSON.stringify({
      title: title,
      desc: desc,
      picture: picture,
      event: event,
    }),
  }).then((response) => {
    if (!response.ok) throw response;
    return response.json();
  });
}
