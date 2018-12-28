import React from 'react';
import logo from './logo.svg';
import classes from './Main.css'

const Main = () => {
    return (
        <div className={classes.App}>
            <header className={classes.header}>
            <img src={logo} className={classes.logo} alt="logo" />
            <h1 className={classes.title}>Welcome to React</h1>
            </header>
            {/* <p className={classes.intro}>
            To get started, edit <code>src/App.js</code> and save to reload.
            </p> */}
            <iframe src='https://webchat.botframework.com/embed/ITQandABot?s=lRv-ZRYBNmA.cwA.er0.pv104-mA0xEzGRCZjSiCKT9y-9wMHW-WboUBP2IIAB8' height="600" width="500">
            </iframe>      
        </div>
    );
}

export default Main;