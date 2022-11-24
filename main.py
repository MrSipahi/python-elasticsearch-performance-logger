import sys

argumentList = sys.argv[1:]



if argumentList[0] == "serviceA":
    from Service.ServiceA import ServiceA
    serviceA = ServiceA()
    serviceA.start()

elif argumentList[0] == "serviceB":
    from Service.ServiceB import ServiceB
    serviceB = ServiceB()
    serviceB.start()