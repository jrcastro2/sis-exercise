import React, { useState } from 'react';
import { Input, Typography, Spin, message, Collapse, Row, Col, Select, Space } from 'antd';
import { searchLiterature } from '../api/literatureApi';

const { Title, Paragraph } = Typography;
const { Option } = Select;
const { Search } = Input;

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [limit, setLimit] = useState(10);

  const handleSearch = async () => {
    if (!query.trim()) {
      message.warning("Please enter a search term.");
      return;
    }

    if (loading) {
      message.warning("Please wait for the current search to finish.");
      return;
    }

    setLoading(true);
    try {
      const data = await searchLiterature(query, limit);
      if (!data.results) {
        message.warning("No results found for the search term.");
      } else {
        setResults(data.results);
        setSummary(data.summary);
      }
    } catch (error) {
      message.error("There was an error fetching data.");
      console.error("Error during search", error);
    } finally {
      setLoading(false);
    }
  };

  const collapseItems = results.map((item, index) => ({
    key: `${index + 1}`,
    label: item.title,
    children: <p>{item.abstract}</p>,
  }));

  return (
    <div >
      <Row justify="space-between" align="middle">
        <Col>
          <Title level={2}>Literature Search</Title>
        </Col>
        <Col>
          <Space>
            <span>Number of results:</span>
            <Select
              defaultValue={10}
              value={limit}
              onChange={(value) => setLimit(value)}
            >
              <Option value={10}>10</Option>
              <Option value={20}>20</Option>
              <Option value={50}>50</Option>
            </Select>
          </Space>
        </Col>
      </Row>

      <Search
        placeholder="Enter a search term"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        enterButton
        onSearch={handleSearch}
        loading={loading}
      />

      {loading && <Spin className='center margin-top-20' />}

      {!loading && summary && (
        <>
          <Title level={4} >Summary</Title>
          <Paragraph>{summary}</Paragraph>
        </>
      )}

      {!loading && results.length > 0 && (
        <>
          <Title level={4} >Results</Title>
          <Collapse items={collapseItems} />
        </>
      )}
    </div>
  );
}

export default App;