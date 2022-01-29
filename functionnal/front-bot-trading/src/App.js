import logo from './logo.svg';
import './App.css';
import { VictoryCandlestick } from 'victory-candlestick';
import { VictoryBar, VictoryChart, VictoryTheme, VictoryAxis } from 'victory';
import { Container, Row, Col } from 'react-bootstrap';
import { useState } from 'react';

let data = [];
let int = undefined
let candle_data = []
function create_left(a, b, c) {
  return (
    <Row>
      <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>{a}</Col>
      <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>{b}</Col>
      <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>{c}</Col>
    </Row>
  )
}

function useForceUpdate(){
  const [value, setValue] = useState(0); // integer state
  return () => setValue(value => value + 1); // update the state to force render
}

function App() {
  const forceUpdate = useForceUpdate();
  clearTimeout(int)
  int = setTimeout(() => {
    fetch('http://localhost:3010/data').then(e => e.json()).then(e => {
      
    data.push(e);
      
      if (data.length > 25) {
        data.shift();
      }
      candle_data = [];
      //{ x: new Date(2016, 6, 2), open: 10, close: 15, high: 20, low: 5 }
      for (let i = 0 ; i < data.length ; i++)
      {
        let t = Date.parse(data[i][1]);
        candle_data.push(
          {
            x: new Date(t),
            open: parseFloat(data[i][3], 10),
            close: parseFloat(data[i][6], 10),
            high: parseFloat(data[i][4], 10),
            low: parseFloat(data[i][5], 10)
          })
        
      }

      forceUpdate();
    })
  }, 1000)
  //const [data, setData] = useState(undefined);
  return (
    <Container className='App' fluid>
      <Row className='nav' style={{ height: '7vh' }}>
        <Col md={{ span: 2, offset: 0 }} style={{ fontWeight: '600', fontSize: '1.2em', marginTop: '1%' }}>TRADOBOT</Col>
      </Row>
      <Row style={{ borderBottom: '1px solid #4c515c', minHeight: '6vh', fontWeight: '600', fontSize: '1.2em', borderTop: 0 }}>
        <Col sm={1}>
          <div>ETH / EUR </div>
          <div style={{ fontWeight: '300', fontSize: '0.8em', marginTop: '1%', color: 'grey' }}>Etherum</div>
        </Col>
        <Col sm={2}>
          <div>Current Price</div>
          <div style={{ fontWeight: '300', fontSize: '0.8em', marginTop: '1%', color: 'green' }}>€3600.45</div>
        </Col>
        <Col sm={2}>
          <div>Variation last hour</div>
          <div style={{ fontWeight: '300', fontSize: '0.8em', marginTop: '1%', color: 'red' }}>6.78%</div>

        </Col>
        <Col sm={2}>
          <div>Bot Base Capital</div>
          <div style={{ fontWeight: '300', fontSize: '0.8em', marginTop: '1%', color: 'red' }}>25 000</div>

        </Col>
        <Col sm={2}>
          <div>Bot Performance</div>
          <div style={{ fontWeight: '300', fontSize: '0.8em', marginTop: '1%', color: 'green' }}>+1800</div>

        </Col>
      </Row>
      <Row >
        <Col style={{ border: '1px solid #4c515c', borderLeft: '0', borderTop: '0', padding: '1%' }}>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '600', fontSize: '1.1em' }}>Tracking</Col>
          </Row>
          <Row style={{ marginTop: '3%' }}>
            <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em' }}>Time</Col>
            <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em' }}>Prix</Col>
            <Col style={{ textAlign: 'left', fontWeight: '300', fontSize: '1.1em' }}>Volume</Col>
          </Row>
          {data.map((e, i) => {
            //console.log(e);
            //create_left(e.date, e.close, e['Volume BTC']);
            return (create_left(e[1].substring(11), e[6].substring(0, 10), e[7].substring(0, 10)))
          })}
        </Col>
        <Col sm={6}>
          <VictoryChart
            theme={VictoryTheme.material}
            domainPadding={{ x: 5 }}
            scale={{ x: "time" }}
          >

            <VictoryAxis dependentAxis />
            <VictoryCandlestick
              candleColors={{ positive: "green", negative: "red" }}
              candleRatio={0.7}
              data={candle_data}
            />
          </VictoryChart>
        </Col>

        <Col style={{ border: '1px solid #4c515c', borderRight: '0', borderTop: '0', padding: '1%' }}>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '600', fontSize: '1.1em' }}>Bot Moves</Col>
          </Row>
          <Row style={{ marginTop: '3%' }}>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em' }}>Type</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em' }}>Price</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em' }}>Volume</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red' }}>Buy</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red' }}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red' }}>0.001</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>Sell</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>3598</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green' }}>0.002</Col>
          </Row>
        </Col>
      </Row>

    </Container>
  );
}

export default App;
