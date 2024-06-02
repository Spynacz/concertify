import { useState } from "react";
import CommentVote from "./CommentVote";

export default function Comment({
  id,
  user,
  desc,
  numVotes,
  hasVoted,
  callback,
}) {
  const [votes, setVotes] = useState(numVotes);
  const [voted, setVoted] = useState(hasVoted);

  return (
    <div className="d-flex my-5">
      <img
        className="rounded-circle me-3"
        style={{ width: "50px", height: "50px" }}
        src="https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-business-user-profile-vector-png-image_1541960.jpg"
      />
      <div className="w-100">
        <h5>{user}</h5>
        <div className="d-flex justify-content-between">
          <p>{desc}</p>
          <CommentVote
            commentId={id}
            voted={voted}
            setVoted={setVoted}
            votes={votes}
            setVotes={setVotes}
            callback={callback}
          />
        </div>
      </div>
    </div>
  );
}
