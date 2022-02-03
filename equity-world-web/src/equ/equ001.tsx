import React, { Component } from "react";
import styled from "styled-components";
import Table from "../com/table";

async function get_remote(path: string) {
  let res = await fetch(
    `https://equityworld-5c018-default-rtdb.asia-southeast1.firebasedatabase.app/${path}.json`
  );
  if (res.status !== 200) throw res.status;
  return await res.json();
}

const TableFloating = styled.div`
  width: 80vmin;
  height: 80vmin;
  border: solid 1px;
  background-color: white;
  box-shadow: 0 0 1rem 0.1rem black;
`;

interface EqutyBase {
  increment: number;
  increment_per: number;
  name: string;
  price: number;
  state: string;
}

interface IProps {
  update_pulse: number;
}
interface IState {
  update_pulse: number;
  crdt?: string;
  eq_bases?: Map<number, EqutyBase>;
}
class App extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = { update_pulse: 0 };
  }

  componentDidUpdate(prevProps: IProps, prevState: IState, snapshot: IState) {
    if (snapshot === undefined) {
      this.on_update_pulse().then((snapshot) => {
        this.setState(snapshot);
      });
    }
  }

  async on_update_pulse() {
    return {
      crdt: await get_remote("crdt"),
      eq_bases: await get_remote("equity_bases"),
    };
  }

  render() {
    return (
      <TableFloating>
        <h1 className="my-2">호반증권({this.state.crdt})</h1>
        <Table
          style={{
            width: "100%",
            flex: "1 1 auto",
          }}
          column_names={["종목명", "금액", "증감", "비고"]}
          column_rows={(function (
            eq_bases: Map<number, EqutyBase> | undefined
          ): Array<Array<string | number>> {
            const result: Array<Array<string | number>> = [];
            if (eq_bases !== undefined)
              eq_bases.forEach((eq_base: EqutyBase) => {
                result.push([
                  eq_base.name,
                  eq_base.price,
                  eq_base.increment,
                  eq_base.state,
                ]);
              });
            return result;
          })(this.state.eq_bases)}
        />
      </TableFloating>
    );
  }
}

export default App;
