import { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import Post from "./Post";
import { getAuthorization } from "../Utils";

export default function PostList({ eventId }) {
  const [posts, setPosts] = useState([]);
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);

  const user = cookies["user"];
  const get = async () => {
    await fetch(`http://localhost:8000/post?event=${eventId}`, {
      method: "GET",
      headers: {
        Authorization: getAuthorization(user),
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then((data) => {
        setPosts(data.results);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    get();
  }, []);

  return (
    <>
      <div className="post-list m-5">
        {posts.map((post) => (
          <Post
            id={post.id}
            title={post.title}
            desc={post.desc}
            votes={post.vote_count}
            image={post.picture}
            hasVoted={post.has_voted}
            key={post.id}
          />
        ))}
      </div>
    </>
  );
}
