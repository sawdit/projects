import React from 'react';
import classes from './Toolbar.css';
import NavigationItems from '../Navigationitems/Navigationitems';

const toolbar =(props) => (
    <header className={classes.Toolbar}>
        <div>MENU</div>
        <div>LOGO</div>
        <nav className={classes.DesktopOnly}>
         <NavigationItems />
        </nav>
    </header>
);

export default toolbar;