from RF24 import RF24
import board
import busio
import digitalio as dio
import argparse

SPI0 = {
    'MOSI':10,#dio.DigitalInOut(board.D10)
    'MISO':9,#dio.DigitalInOut(board.D9)
    'clock':11,#dio.DigitalInOut(board.D11)
    'ce':dio.DigitalInOut(board.D17),
    'csn':dio.DigitalInOut(board.D8)
    }
SPI1 = {
    'MOSI':20,#dio.DigitalInOut(board.D20)
    'MISO':19,#dio.DigitalInOut(board.D19)
    'clock':21,#dio.DigitalInOut(board.D21)
    "ce":dio.DigitalInOut(board.D27),
    'csn':dio.DigitalInOut(board.D18)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NRF24L01+ test')
    parser.add_argument('--src', dest='src', type=str, default='me', help='NRF24L01+\'s source address')
    parser.add_argument('--dst', dest='dst', type=str, default='me', help='NRF24L01+\'s destination address')
    parser.add_argument('--count', dest='cnt', type=int, default=10, help='Number of transmissions')
    parser.add_argument('--size', dest='size', type=int, default=32, help='Packet size')
    parser.add_argument('--txchannel', dest='txchannel', type=int, default=76, help='Tx channel', choices=range(0,125))
    parser.add_argument('--rxchannel', dest='rxchannel', type=int, default=76, help='Rx channel', choices=range(0,125))

    args = parser.parse_args()

    SPI0['spi'] = busio.SPI(**{x: SPI0[x] for x in ['clock', 'MOSI', 'MISO']})
    SPI1['spi'] = busio.SPI(**{x: SPI1[x] for x in ['clock', 'MOSI', 'MISO']})

    # initialize the nRF24L01 on the spi bus object

    print(SPI0["ce"], SPI1["ce"])
    #rx_nrf = RF24(**{x: SPI0[x] for x in ['spi', 'csn', "ce"]})
    rx_nrf = RF24(SPI0['spi'], SPI0['csn'], SPI0['ce'])
    
    #tx_nrf = RF24(**{x: SPI1[x] for x in ['spi', 'csn', "ce"]})
    tx_nrf = RF24(SPI1['spi'], SPI1['csn'], SPI1['ce'])

    print(f'nRF24L01+ found on SPI0: {rx_nrf}, SPI1: {tx_nrf}')
