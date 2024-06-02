import { useEffect, useState } from "react";
import { Button, Card, Col, Nav, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import Post from "./Post";

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
            numVotes={post.vote_count}
            image={post.picture}
            hasVoted={post.has_voted}
            key={post.id}
          />
        ))}
      </div>
    </>
  );
}
