import React, { Component } from 'react';
import logo from './../logo.svg';
import './App.css';
import Bar from './../components/Bar/Bar';

class App extends Component {
  state = {
    buttons: [
      {top: "Search"},
      {middle: "Login"},
      {bottom: "Do"}
    ]
  }

  changeButtonStateTopHandler = () => {
    this.setState( {
      buttons: [
        {top: "Login"},
        {middle: "Search"},
        {bottom: "Do"}
      ]
    })
  }

  changeButtonStateMiddleHandler = () => {
    this.setState( {
      buttons: [
        {top: "Search"},
        {middle: "Login"},
        {bottom: "Do"}
      ]
    })
  }

  changeButtonStateBottomHandler = () => {
    this.setState( {
      buttons: [
        {top: "Search"},
        {middle: "Do"},
        {bottom: "Login"}
      ]
    })
  }

  render() {
    let logicbar =  (
      <Bar clickTop={this.changeButtonStateTopHandler} clickBottom={this.changeButtonStateBottomHandler} top={this.state.buttons[0].top} middle={this.state.buttons[1].middle} bottom={this.state.buttons[2].bottom}/>
      );

    if (this.state.buttons[1].middle === "Login") {
      logicbar =  (
      <Bar clickTop={this.changeButtonStateTopHandler} clickBottom={this.changeButtonStateBottomHandler} top={this.state.buttons[0].top} middle={this.state.buttons[1].middle} bottom={this.state.buttons[2].bottom}/>
      );
      console.log("Login");
    }

    if (this.state.buttons[1].middle === "Search") {
      logicbar = (
      <Bar clickTop={this.changeButtonStateMiddleHandler} clickBottom={this.changeButtonStateBottomHandler} top={this.state.buttons[0].top} middle={this.state.buttons[1].middle} bottom={this.state.buttons[2].bottom}/>
      );
      console.log("Search");
    }

    if (this.state.buttons[1].middle === "Do") {
      logicbar = (
      <Bar clickTop={this.changeButtonStateTopHandler} clickBottom={this.changeButtonStateMiddleHandler} top={this.state.buttons[0].top} middle={this.state.buttons[1].middle} bottom={this.state.buttons[2].bottom}/>
      );
      console.log("Do");
    }

    return (
       <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        {logicbar}
      </div>
    );
  }
}

export default App;
