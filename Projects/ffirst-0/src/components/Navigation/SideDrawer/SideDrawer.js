import React from 'react';
import classes from './SideDrawer.css'
import NavigationItems from '../Navigationitems/Navigationitems';

const sideDrawer = (props) => {
    return (
        <div className={classes.SideDrawer}>
            <nav>
                <NavigationItems />
            </nav>
        </div>
    );
};

export default sideDrawer;