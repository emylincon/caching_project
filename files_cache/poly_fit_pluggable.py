import numpy 


def _eval(coef, t):     
    global eqn
    # print('\ncoef : ', coef)
    eqn = f = numpy.poly1d(coef)
    return f(t)


def predict(t_series, deg):
    x = numpy.arange(len(t_series))
    # print('\nx=',x)
    coef = list(numpy.polyfit(x, t_series, deg))
    return _eval(coef, len(t_series)+1)


def main(t_series, deg):
    return predict(t_series, deg)


    



