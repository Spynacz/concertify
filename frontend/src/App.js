import React from 'react';
import {useRef} from 'react';
import {useState} from 'react';
import {useEffect} from 'react';
import './App.css';
import NavBar from './NavBar';
import { EventList } from './Event';

export default function App() {
  return (
    <>
      <NavBar isGuest={true}/>
      <EventList count={25}/>
    </>
  );
}
