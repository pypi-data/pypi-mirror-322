import numpy as np
import pandas as pd
import re
import xarray as xr

# with open('f74113.dat', 'r') as f:
#     lines = [line.strip().split() for line in f.readlines()]
#     waves = [float(l.pop(0)) for l in lines]
#     lines2 = [''.join(i) for i in lines]
#
#     print(lines2)
#
#     fluxes = []
#     elements = []
#     notes = []
#
#     for l in lines2:
#         index = l.rfind('.') + 2
#
#         print(l[:index], l[index:])
#         fluxes.append(float(l[:index]))
#
#         if l[-1] == 'B' or l[-1] == 'G' or l[-1] == '?':
#             notes.append(l[-1])
#             elements.append(l[index:-1])
#         else:
#             notes.append('None')
#             elements.append(l[index:])
#
#
#
# data = pd.DataFrame({'waves':waves,
#                      'flux': fluxes,
#                      'element': elements,
#                      'notes': notes})
# data.to_csv('f74113.csv', index=False)
# print(data.dtypes)
# x = xr.Dataset().from_dataframe(data)
# print(x)


# with open('r74113.dat', 'r') as f:
#     lines = [line.strip().split() for line in f.readlines()]
#     waves = [float(l.pop(0)) for l in lines]
#     lines2 = [''.join(i) for i in lines]
#     print(lines2)
#
#     fluxes = []
#     elements = []
#     notes = []
#
#     for l in lines2:
#         index = l.rfind('.') + 2
#
#         print(l[:index], l[index:])
#         fluxes.append(float(l[:index]))
#
#         if l[-1] == 'B' or l[-1] == 'G' or l[-1] == '?':
#             notes.append(l[-1])
#             elements.append(l[index:-1])
#         else:
#             notes.append('None')
#             elements.append(l[index:])
#
#
#
# data = pd.DataFrame({'waves':waves,
#                      'flux': fluxes,
#                      'element': elements,
#                      'notes': notes})
# data.to_csv('r74113.csv', index=False)
# print(data.dtypes)
# x = xr.Dataset().from_dataframe(data)
# print(x)

# with open('f76ref.dat', 'r') as f:
#     fluxes = []
#     elements = []
#     notes = []
#     K = []
#     C = []
#
#     lines = [line.strip().split() for line in f.readlines()]
#     # print(lines)
#     C = [float(line.pop(-1)) for line in lines]
#     K = [float(line.pop(-1)) for line in lines]
#
#     waves = [float(l.pop(0)) for l in lines]
#     lines2 = [''.join(i) for i in lines]
#     print(lines2)
#
#     for l in lines2:
#         index = l.rfind('.') + 2
#
#         print(l[:index], l[index:])
#         fluxes.append(float(l[:index]))
#
#         if l[-1] == 'B' or l[-1] == 'G' or l[-1] == '?':
#             notes.append(l[-1])
#             elements.append(l[index:-1])
#         else:
#             notes.append('None')
#             elements.append(l[index:])
#
#
#
# data = pd.DataFrame({'waves':waves,
#                      'flux': fluxes,
#                      'element': elements,
#                      'notes': notes,
#                      'K': K,
#                      'C':C})
# data.to_csv('f76ref.csv', index=False)
# print(data.dtypes)
# x = xr.Dataset().from_dataframe(data)
# print(x)

# with open('sc21refw.dat', 'r') as f:
#     fluxes = []
#     elements = []
#     notes = []
#     K = []
#     C = []
#
#     lines = [line.strip().split() for line in f.readlines()]
#     # print(lines)
#     C = [float(line.pop(-1)) for line in lines]
#     K = [float(line.pop(-1)) for line in lines]
#
#     waves = [float(l.pop(0)) for l in lines]
#     lines2 = [''.join(i) for i in lines]
#     print(lines2)
#
#     for l in lines2:
#         index = l.rfind('.') + 2
#
#         print(l[:index], l[index:])
#         fluxes.append(float(l[:index]))
#
#         if l[-1] == 'B' or l[-1] == 'G' or l[-1] == '?':
#             notes.append(l[-1])
#             elements.append(l[index:-1])
#         else:
#             notes.append('None')
#             elements.append(l[index:])
#
# data = pd.DataFrame({'waves':waves,
#                      'flux': fluxes,
#                      'element': elements,
#                      'notes': notes,
#                      'K': K,
#                      'C':C})
# data.to_csv('sc21refw.csv', index=False)
# print(data.dtypes)
# x = xr.Dataset().from_dataframe(data)
# print(x)

# data = pd.read_csv('r74113.csv')
# x = xr.Dataset().from_dataframe(data)
# x.to_netcdf('r74113.nc')
