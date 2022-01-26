import logo from './logo.svg';
import './App.css';
import { VictoryCandlestick } from 'victory-candlestick';
import { VictoryBar, VictoryChart, VictoryTheme, VictoryAxis } from 'victory';
import { Container, Row, Col } from 'react-bootstrap';

function App() {
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
      <Row>
        <Col style={{ border: '1px solid #4c515c', borderLeft: '0', borderTop: '0', padding: '1%'}}>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '600', fontSize: '1.1em'}}>Tracking</Col>
          </Row>
          <Row style={{marginTop: '3%'}}>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Time</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Prix</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Volume</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>20:45:15</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>799999</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>20:45:15</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>799999</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>20:45:15</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>799999</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>20:45:15</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>799999</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>20:45:15</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>799999</Col>
          </Row>
        </Col>
        <Col sm={6}>
          <VictoryChart
            theme={VictoryTheme.material}
            domainPadding={{ x: 10 }}
            scale={{ x: "time" }}
          >

            <VictoryAxis dependentAxis />
            <VictoryCandlestick
              candleColors={{ positive: "green", negative: "red" }}
              candleRatio={0.2}
              data={[
                { x: new Date(2016, 6, 1), open: 5, close: 10, high: 15, low: 0 },
                { x: new Date(2016, 6, 2), open: 10, close: 15, high: 20, low: 5 },
                { x: new Date(2016, 6, 3), open: 15, close: 20, high: 22, low: 10 },
                { x: new Date(2016, 6, 4), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 6), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 7), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 8), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 9), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 10), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 11), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 12), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 13), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 14), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 15), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 16), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 17), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 18), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 19), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 20), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 21), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 22), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 23), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 24), open: 20, close: 10, high: 25, low: 7 },
                { x: new Date(2016, 6, 25), open: 10, close: 8, high: 15, low: 5 }
              ]}
            />
          </VictoryChart>
        </Col>
        
        <Col style={{ border: '1px solid #4c515c', borderRight: '0', borderTop: '0', padding: '1%'}}>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '600', fontSize: '1.1em'}}>Bot Moves</Col>
          </Row>
          <Row style={{marginTop: '3%'}}>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Type</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Price</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em'}}>Volume</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red'}}>Buy</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red'}}>3600</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'red'}}>0.001</Col>
          </Row>
          <Row>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>Sell</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>3598</Col>
            <Col style={{ textAlign: 'center', fontWeight: '300', fontSize: '1.1em', color: 'green'}}>0.002</Col>
          </Row>
        </Col>
      </Row>

    </Container>
  );
}

export default App;
