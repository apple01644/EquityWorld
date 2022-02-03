import React, { Component, CSSProperties } from "react";
import styled from "styled-components";

const Table = styled.table`
  border: solid 1px;
`;

const Th = styled.th`
  border: solid 1px;
`;

const Td = styled.td`
  border: solid 1px;
`;

interface IProps {
  style?: CSSProperties;
  column_names: Array<string>;
  column_rows: Array<Array<string | number>>;
}
interface IState {}
class App extends Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <Table style={this.props.style}>
          <thead>
            {this.props.column_names.map((column_name) => (
              <Th>{column_name}</Th>
            ))}
          </thead>
          <tbody>
            {this.props.column_rows.map((row) => (
              <tr>
                {row.map((value) => (
                  <Td>{value}</Td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    );
  }
}

export default App;
