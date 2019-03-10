import React, { Component } from 'react';
import APICredentials from './secret';


class App extends Component {

  constructor(props){
    super(props)
    this.state = {
      locationID : '',
      A : {
        x : '',
        y : '',
        capacity: '',
        tolerance: '',
      },
      B : {
        x : '',
        y : '',
        capacity: '',
        tolerance: '',
      }
    }
  }

  submitHelper = (event) => {
    let input = {
      locationID : this.state.locationID,
      keys : {
        A: this.state.A,
        B: this.state.B
      }
    }
    const Request = new XMLHttpRequest();
    Request.open('POST', 'https://api.mlab.com/api/1/databases/aiaa/collections/Geo?apiKey='+APICredentials.mLab, true)
    Request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    alert((Request.send(JSON.stringify(input))).status())
  }

  handleLocationID = (event) => {
    this.setState({
      locationID : event.target.value
    })
  }

  handleAx = (event) =>{
    this.setState({
      A : {
        x : event.target.value
      }
    })
  }

  handleBx = (event) =>{
    this.setState({
      B : {
        x : event.target.value
      }
    }) 
  }

  handleAy = (event) =>{
    this.setState({
      A : {
        y : event.target.value
      }
    })
  }

  handleBy = (event) =>{
    this.setState({
      B : {
        y : event.target.value
      }
    })    
  }

  handleAcapacity = (event) => {
    this.setState({
      A : {
        capacity : event.target.value
      }
    })
  }

  handleBcapacity = (event) => {
    this.setState({
      B : {
        capacity : event.target.value
      }
    })
  }

  handleAtolerance = (event) => {
    this.setState({
      A : {
        tolerance : event.target.value
      }
    })
  }

  handleBtolerance = (event) => {
    this.setState({
      B : {
        tolerance : event.target.value
      }
    })
  }


  render() {
    return (
     <div>
     <h1>Database Population Form</h1>
     <br/>
     <form onSubmit = {this.submitHelper}>
     <label>
      locationID
      <input type="text" value={this.state.value} onChange={this.handleLocationID} />
     </label>
     <label>
      A.x
      <input type="text" value={this.state.value} onChange={this.handleAx} />
     </label>
     <label>
      A.y
      <input type="text" value={this.state.value} onChange={this.handleAy} />
     </label>
     <label>
      A.capacity
      <input type="text" value={this.state.value} onChange={this.handleAcapacity} />
     </label>
     <label>
      A.tolerance
      <input type="text" value={this.state.value} onChange={this.handleAtolerance} />
     </label>
     <label>
      B.x
      <input type="text" value={this.state.value} onChange={this.handleBx} />
     </label>
     <label>
      B.y
      <input type="text" value={this.state.value} onChange={this.handleBy} />
     </label>
     <label>
      B.capacity
      <input type="text" value={this.state.value} onChange={this.handleBcapacity} />
     </label>
     <label>
      B.tolerance
      <input type="text" value={this.state.value} onChange={this.handleBtolerance} />
     </label>
     <input type="submit" value="Submit" />
     </form>
     </div>
    );
  }
}

export default App;