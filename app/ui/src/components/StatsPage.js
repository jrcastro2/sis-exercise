import React, { Component } from 'react';
import { Table, Card, Tag } from 'antd';
import { getUserQueries, getOpenAIMetrics } from '../api/metricsApi';

class StatsPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            userQueries: [],
            openAIMetrics: {},
        };
    }

    componentDidMount() {
        getUserQueries().then(data => {
            const rankedData = data.map((item, index) => ({
                ...item,
                rank: index + 1,
            }));
            this.setState({ userQueries: rankedData });
        });

        getOpenAIMetrics().then(data => {
            this.setState({ openAIMetrics: data });
        });
    }

    render() {
        const { userQueries, openAIMetrics } = this.state;

        const userQueryColumns = [
            { title: 'Rank', dataIndex: 'rank', key: 'rank' },
            { title: 'Query', dataIndex: 'query', key: 'query' },
            { title: 'Count', dataIndex: 'query_count', key: 'query_count' },
        ];

        return (
            <div>
                <h1>Metrics Dashboard</h1>
                <h2>OpenAI Metrics</h2>

                <div className='display-flex center'>
                    <Card className='width-33-p padding-5'>
                        <h3>{openAIMetrics.average_response_time || 'N/A'} miliseconds</h3>
                        <Tag color="gold">Average Response Time</Tag>
                    </Card>

                    <Card className='width-33-p padding-5'>
                        <h3>{openAIMetrics.fastest_response_time || 'N/A'} miliseconds</h3>
                        <Tag color="green">Fastest Response Time</Tag>
                    </Card>

                    <Card className='width-33-p padding-5'>
                        <h3>{openAIMetrics.slowest_response_time || 'N/A'} miliseconds</h3>
                        <Tag color="volcano">Slowest Response Time</Tag>
                    </Card>

                </div>
                <h2>User Queries</h2>
                <Table pagination={false} dataSource={userQueries} columns={userQueryColumns} rowKey="query" />

            </div>
        );
    }
}

export default StatsPage;