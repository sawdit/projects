import React from 'react';
import classes from './Navigationitems.css';
import NavigationItem from './Navigationitem/Navigationitem';

const navigationItems = () => (
    <ul className={classes.NavigationItems}>
        <NavigationItem link="/">Profile</NavigationItem>
        <NavigationItem link="/" active>Family</NavigationItem>
        <NavigationItem link="/">Friends</NavigationItem>
        <NavigationItem link="/">Pets</NavigationItem>
        <NavigationItem link="/">Appointments</NavigationItem>
        <NavigationItem link="/">Activities</NavigationItem>
    </ul>
);

export default navigationItems;