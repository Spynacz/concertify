import './NavBar.css'

function UserNavBar() {
  return  (
    <ul>
      <li>New Event</li>
    <li>Cart</li>
    <li>Profile</li>
    <li>Logout</li>
    </ul>
);
}

function GuestNavBar() {
  return  (
    <ul>
      <li>Cart</li>
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
