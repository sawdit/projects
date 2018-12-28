import React from 'react';

const bar = (props) => {
    return (
        <form>
          <div className="App-bar-container">
            <input className="App-bar-options" type="button" value={props.top} onClick={props.clickTop}/>
            <input className="App-bar" type="text" name="login" placeholder={props.middle}/>
            <input className="App-bar-options" type="button" value={props.bottom} onClick={props.clickBottom}/>
          </div>
        </form>
    )
};

export default bar;