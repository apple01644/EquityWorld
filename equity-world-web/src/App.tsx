import React, { Component } from "react";
import "./App.css";
import Equ001 from "./equ/equ001";

interface IProps {}
interface IState {
  update_pulse: number;
}
class App extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {
      update_pulse: 0,
    };
  }

  componentDidMount() {
    setInterval(() => this.on_raise(), 500);
  }

  on_raise() {
    let snapshot = { update_pulse: this.state.update_pulse + 1 };

    this.setState(snapshot);
  }
  render() {
    return (
      <div className="App">
        <Equ001 update_pulse={this.state.update_pulse} />
      </div>
    );
  }
}

export default App;
