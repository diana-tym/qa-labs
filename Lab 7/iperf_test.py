import parser

class TestSuite():
    def test_iperf3(self, client):
        stdout, error_cl, error_serv = client
        
        print(f'Server error: {error_serv}')
        print(f'Client error: {error_cl}')
        print(f'Results: {stdout}')
        
        assert not error_cl
        iperf_results = parser.parse(stdout)
        for value in iperf_results:
            assert value['Transfer'] > 2 and value['Bitrate'] > 20

