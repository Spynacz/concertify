import { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import { getAuthorization } from "../Utils";

export default function PostVote({ postId, voted, setVoted, votes, setVotes }) {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);

  const user = cookies["user"];

  const handle = () => {
    voted ? handleDownvote() : handleUpvote();
  };

  const handleUpvote = async () => {
    await fetch("http://localhost:8000/post-vote", {
      method: "POST",
      headers: {
        Authorization: getAuthorization(user),
        "Content-type": "application/json; charset=UTF=8",
      },
      body: JSON.stringify({
        post: postId,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        setVoted(true);
        setVotes(votes + 1);
        return response.json();
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const handleDownvote = async () => {
    await fetch("http://localhost:8000/post-vote", {
      method: "DELETE",
      headers: {
        Authorization: getAuthorization(user),
        "Content-type": "application/json; charset=UTF=8",
      },
      body: JSON.stringify({
        post: postId,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.status);
        setVoted(false);
        setVotes(votes - 1);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <button
      onClick={(e) => {
        e.stopPropagation();
        handle();
      }}
    >
      <span className="ms-3" style={{ whiteSpace: "nowrap" }}>
        {voted ? (
          <i className="fas fa-thumbs-up"></i>
        ) : (
          <i className="far fa-thumbs-up"></i>
        )}{" "}
        {votes}
      </span>
    </button>
  );
}
