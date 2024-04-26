import { useEffect, useState } from "react";

export default function PostList({ eventId }) {
  const [posts, setPosts] = useState([]);

  const get = async () => {
    await fetch(`http://localhost:8000/post?event=${eventId}`, {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setPosts(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    get();
  }, []);

  return <div>Post List. TBI</div>;
}
