import './NavBar.css'

function SharedNavBar() {
  return (
    <>
      <li>Search</li>
      <li>Cart</li>
    </>
  );
}

function UserNavBar() {
  return  (
    <ul>
      <SharedNavBar/>
      <li>New Event</li>
      <li>Profile</li>
      <li>Logout</li>
    </ul>
  );
}

function GuestNavBar() {
  return  (
    <ul>
      <SharedNavBar/>
      <li>Login</li>
      <li>Register</li>
    </ul>
);
}

export default function NavBar({ isGuest }) {
  return  (
    <div id="navbar">
      <div id="logo">concertify</div>
           {
             isGuest ?
               (<GuestNavBar/>)
               :
               (<UserNavBar/>)
                 }
    </div>
  );
}
