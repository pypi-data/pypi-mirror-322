from ....device import DEV_CPU as DEV_CPU
from ....dtype import C_DTYPE as C_DTYPE, D_DTYPE as D_DTYPE, get_readable_dtype_str as get_readable_dtype_str, kcomplex64 as kcomplex64
from ....nn.parameter import Parameter as Parameter
from ....nn.torch import TorchModule as TorchModule
from ....tensor import QTensor as QTensor
from ....utils.initializer import quantum_uniform as quantum_uniform
from ...hybird_vqc_qpanda import HybirdVQCQpandaQVMLayer as NHybirdVQCQpandaQVMLayer
from ...pq_utils import PQ_QCLOUD_UTILS as PQ_QCLOUD_UTILS
from ...quantumlayer import QuantumBatchAsyncQcloudLayer as NQuantumBatchAsyncQcloudLayer, QuantumLayerV2 as NQuantumLayerV2
from ..qcircuit import vqc_to_originir_list as vqc_to_originir_list
from .utils import complex_dtype_to_float_dtype as complex_dtype_to_float_dtype
from _typeshed import Incomplete
from collections import defaultdict as defaultdict, deque as deque
from typing import Callable
from unittest.mock import Mock as torch

class _TorchQuantumLayer(TorchModule): ...

class TorchQcloudQuantumLayer(_TorchQuantumLayer, NQuantumBatchAsyncQcloudLayer):
    '''

    A torch.nn.module that can use originqc qcloud to do vqc training.
    Abstract Calculation module for originqc real chip using pyqpanda QCLOUD from version 3.8.2.2. It submit parameterized quantum
    circuits to real chip and get the measurement result.

    :param origin_qprog_func: callable quantum circuits function constructed by QPanda.
    :param qcloud_token: `str` - Either the type of quantum machine or the cloud token for execution.
    :param para_num: `int` - Number of parameters; parameters are one-dimensional.
    :param num_qubits: `int` - Number of qubits in the quantum circuit.
    :param num_cubits: `int` - Number of classical bits for measurement in the quantum circuit.
    :param pauli_str_dict: `dict|list` - Dictionary or list of dictionary representing the Pauli operators in the quantum circuit. Default is None.
    :param shots: `int` - Number of measurement shots. Default is 1000.
    :param initializer: Initializer for parameter values. Default is None.
    :param dtype: Data type of parameters. Default is None, which uses the default data type.
    :param name: Name of the module. Default is an empty string.
    :param diff_method: Differentiation method for gradient computation. Default is "parameter_shift".
    IF diff_method == "random_coordinate_descent", we will random choice single parameters to calculate gradients, other will keep zero. reference: https://arxiv.org/abs/2311.00088
    :param submit_kwargs: Additional keyword arguments for submitting quantum circuits,
    default:{"chip_id":pyqpanda.real_chip_type.origin_72,"is_amend":True,"is_mapping":True,
    "is_optimization": True,"default_task_group_size":200,"test_qcloud_fake":True}.
    :param query_kwargs: Additional keyword arguments for querying quantum results，default:{"timeout":2,"print_query_info":True,"sub_circuits_split_size":1}.
    :return: A module that can calculate quantum circuits.
    Example::

    
        import pyqpanda as pq
        import pyvqnet
        from pyvqnet.qnn.vqc.torch import TorchQcloudQuantumLayer

        pyvqnet.backends.set_backend("torch")
        def qfun(input,param, m_machine, m_qlist,cubits):
            measure_qubits = [0,2]
            m_prog = pq.QProg()
            cir = pq.QCircuit()
            cir.insert(pq.RZ(m_qlist[0],input[0]))
            cir.insert(pq.CNOT(m_qlist[0],m_qlist[1]))
            cir.insert(pq.RY(m_qlist[1],param[0]))
            cir.insert(pq.CNOT(m_qlist[0],m_qlist[2]))
            cir.insert(pq.RZ(m_qlist[1],input[1]))
            cir.insert(pq.RY(m_qlist[2],param[1]))
            cir.insert(pq.H(m_qlist[2]))
            m_prog.insert(cir)

            for idx, ele in enumerate(measure_qubits):
                m_prog << pq.Measure(m_qlist[ele], cubits[idx])  # pylint: disable=expression-not-assigned
            return m_prog

        l = TorchQcloudQuantumLayer(qfun,
                        "3047DE8A59764BEDAC9C3282093B16AF1",
                        2,
                        6,
                        6,
                        pauli_str_dict=None,
                        shots = 1000,
                        initializer=None,
                        dtype=None,
                        name="",
                        diff_method="parameter_shift",
                        submit_kwargs={"test_qcloud_fake":True},
                        query_kwargs={})
        x = pyvqnet.tensor.QTensor([[0.56,1.2],[0.56,1.2],[0.56,1.2],[0.56,1.2],[0.56,1.2]],requires_grad= True)
        y = l(x)
        print(y)
        y.backward()
        print(l.m_para.grad)
        print(x.grad)

        def qfun2(input,param, m_machine, m_qlist,cubits):
            measure_qubits = [0,2]
            m_prog = pq.QProg()
            cir = pq.QCircuit()
            cir.insert(pq.RZ(m_qlist[0],input[0]))
            cir.insert(pq.CNOT(m_qlist[0],m_qlist[1]))
            cir.insert(pq.RY(m_qlist[1],param[0]))
            cir.insert(pq.CNOT(m_qlist[0],m_qlist[2]))
            cir.insert(pq.RZ(m_qlist[1],input[1]))
            cir.insert(pq.RY(m_qlist[2],param[1]))
            cir.insert(pq.H(m_qlist[2]))
            m_prog.insert(cir)

            return m_prog
        l = TorchQcloudQuantumLayer(qfun2,
                "3047DE8A59764BEDAC9C3282093B16AF",
                2,
                6,
                6,
                pauli_str_dict={\'Z0 X1\':10,\'\':-0.5,\'Y2\':-0.543},
                shots = 1000,
                initializer=None,
                dtype=None,
                name="",
                diff_method="parameter_shift",
                submit_kwargs={"test_qcloud_fake":True},
                query_kwargs={})
        x = pyvqnet.tensor.QTensor([[0.56,1.2],[0.56,1.2],[0.56,1.2],[0.56,1.2]],requires_grad= True)
        y = l(x)
        print(y)
        y.backward()
        print(l.m_para.grad)
        print(x.grad)

    '''
    m_prog_func: Incomplete
    pauli_str_dict: Incomplete
    pq_utils: Incomplete
    submit_kwargs: Incomplete
    query_kwargs: Incomplete
    shots: Incomplete
    m_machine: Incomplete
    qlists: Incomplete
    clists: Incomplete
    def __init__(self, origin_qprog_func: Callable, qcloud_token: str, para_num: int, num_qubits: int, num_cubits: int, pauli_str_dict: list[dict] | dict | None = None, shots: int = 1000, initializer: Callable = None, dtype: int | None = None, name: str = '', diff_method: str = 'parameter_shift', submit_kwargs: dict = {}, query_kwargs: dict = {}) -> None: ...
    def forward(self, x: QTensor): ...

class QcloudFunctionHelper(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, weights, qlayer): ...
    @staticmethod
    def backward(ctx, grad_output): ...

class TorchQpandaQuantumLayer(_TorchQuantumLayer, NQuantumLayerV2):
    '''
    torch api for quantumlayerv2

    Calculation module for Variational Quantum Layer. It simulate a parameterized quantum
    circuit and get the measurement result. It inherits from Module,so that it can calculate
    gradients of circuits parameters,and trains Variational Quantum Circuits model or embeds
    Variational Quantum Circuits into hybird Quantum and Classic model.

    You need to allocated simulation machine and qubits by yourself.

    :param qprog_with_measure: callable quantum circuits functions ,cosntructed by qpanda
    :param para_num: `int` - Number of parameter
    :param diff_method: \'parameter_shift\' or \'finite_diff\'
    :param delta:  delta for diff

    :param dtype: data type of parameters,default: None,use default data type.
    :param name: name of module,default:"".
    :return: a module can calculate quantum circuits .

    Note:
        qprog_with_measure is quantum circuits function defined in pyQPanda :
         https://pyqpanda-toturial.readthedocs.io/zh/latest/QCircuit.html.

        This function should contains following parameters,otherwise it can not run
         properly in TorchQpandaQuantumLayer.

        Compare to QuantumLayer.you should allocate qubits and simulator:
         https://pyqpanda-toturial.readthedocs.io/zh/latest/QuantumMachine.html,

        you may also need to allocate cubits if qprog_with_measure needs quantum
         measure:https://pyqpanda-toturial.readthedocs.io/zh/latest/Measure.html

        qprog_with_measure (input,param)

            `input`: array_like input 1-dim classic data

            `param`: array_like input 1-dim quantum circuit\'s parameters

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn import ProbsMeasure
        import numpy as np
        from pyvqnet.tensor import QTensor
        import pyvqnet
        pyvqnet.backends.set_backend("torch")
        from pyvqnet.qnn.vqc.torch import TorchQpandaQuantumLayer
        def pqctest (input,param):
            num_of_qubits = 4

            m_machine = pq.CPUQVM()# outside
            m_machine.init_qvm()# outside
            qubits = m_machine.qAlloc_many(num_of_qubits)

            circuit = pq.QCircuit()
            circuit.insert(pq.H(qubits[0]))
            circuit.insert(pq.H(qubits[1]))
            circuit.insert(pq.H(qubits[2]))
            circuit.insert(pq.H(qubits[3]))

            circuit.insert(pq.RZ(qubits[0],input[0]))
            circuit.insert(pq.RZ(qubits[1],input[1]))
            circuit.insert(pq.RZ(qubits[2],input[2]))
            circuit.insert(pq.RZ(qubits[3],input[3]))

            circuit.insert(pq.CNOT(qubits[0],qubits[1]))
            circuit.insert(pq.RZ(qubits[1],param[0]))
            circuit.insert(pq.CNOT(qubits[0],qubits[1]))

            circuit.insert(pq.CNOT(qubits[1],qubits[2]))
            circuit.insert(pq.RZ(qubits[2],param[1]))
            circuit.insert(pq.CNOT(qubits[1],qubits[2]))

            circuit.insert(pq.CNOT(qubits[2],qubits[3]))
            circuit.insert(pq.RZ(qubits[3],param[2]))
            circuit.insert(pq.CNOT(qubits[2],qubits[3]))
            #print(circuit)

            prog = pq.QProg()
            prog.insert(circuit)

            rlt_prob = ProbsMeasure([0,2],prog,m_machine,qubits)
            return rlt_prob

        pqc = TorchQpandaQuantumLayer(pqctest,3)

        #classic data as input
        input = QTensor([[1.0,2,3,4],[4,2,2,3],[3,3,2,2]],requires_grad=True)

        #forward circuits
        rlt = pqc(input)

        print(rlt)

        grad =  QTensor(np.ones(rlt.data.shape)*1000)
        #backward circuits
        rlt.backward(grad)

        print(pqc.m_para.grad)
        print(input.grad)


    '''
    m_prog_func: Incomplete
    delta: Incomplete
    def __init__(self, qprog_with_measure: Callable, para_num: int, diff_method: str = 'parameter_shift', delta: float = 0.01, dtype: int | None = None, name: str = '') -> None: ...
    def forward(self, x: QTensor): ...

class TorchFunctionHelper(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, weights, qlayer): ...
    @staticmethod
    def backward(ctx, grad_output): ...

class HybirdVQCQpandaQVMLayer(TorchModule, NHybirdVQCQpandaQVMLayer):
    '''
    Torch backend api for HybirdVQCQpandaQVMLayer.
    
    Hybird vqc and qpanda QVM layer.use qpanda qvm to run forward and use vqc to calculate gradients.

    :param vqc_module: vqc_module with forward(), qmachine is correctly set.
    :param qcloud_token: `str` - Either the type of quantum machine or the cloud token for execution.
    :param num_qubits: `int` - Number of qubits in the quantum circuit.
    :param num_cubits: `int` - Number of classical bits for measurement in the quantum circuit.
    :param pauli_str_dict: `dict|list` - Dictionary or list of dictionary representing the Pauli operators in the quantum circuit. Default is None.
    :param shots: `int` - Number of measurement shots. Default is 1000.
    :param name: Name of the module. Default is an empty string.
    :param submit_kwargs: Additional keyword arguments for submitting quantum circuits,
    default:{"chip_id":pyqpanda.real_chip_type.origin_72,"is_amend":True,"is_mapping":True,
    "is_optimization": True,"default_task_group_size":200,"test_qcloud_fake":True}.
    :param query_kwargs: Additional keyword arguments for querying quantum results，default:{"timeout":2,"print_query_info":True,"sub_circuits_split_size":1}.
    :return: A module that can calculate quantum circuits.

    .. note::
        pauli_str_dict should not be None, and it should be same as obs in vqc_module measure function.
        vqc_module should have attribute with type of QMachine, QMachine should set save_ir=True

    Example::

        import pyvqnet.backends
        import numpy as np
        from pyvqnet.qnn.vqc.torch import QMachine,QModule,RX,RY,        RZ,U1,U2,U3,I,S,X1,PauliX,PauliY,PauliZ,SWAP,CZ,        RXX,RYY,RZX,RZZ,CR,Toffoli,Hadamard,T,CNOT,MeasureAll,        TorchHybirdVQCQpandaQVMLayer
        import pyvqnet
        
        from pyvqnet import tensor

        import pyvqnet.utils
        pyvqnet.backends.set_backend("torch")
        pyvqnet.utils.set_random_seed(42)

        class QModel(QModule):
            def __init__(self, num_wires, dtype,grad_mode=""):
                super(QModel, self).__init__()

                self._num_wires = num_wires
                self._dtype = dtype
                self.qm = QMachine(num_wires, dtype=dtype,grad_mode=grad_mode,save_ir=True)
                self.rx_layer = RX(has_params=True, trainable=False, wires=0)
                self.ry_layer = RY(has_params=True, trainable=False, wires=1)
                self.rz_layer = RZ(has_params=True, trainable=False, wires=1)
                self.u1 = U1(has_params=True,trainable=True,wires=[2])
                self.u2 = U2(has_params=True,trainable=True,wires=[3])
                self.u3 = U3(has_params=True,trainable=True,wires=[1])
                self.i = I(wires=[3])
                self.s = S(wires=[3])
                self.x1 = X1(wires=[3])
                
                self.x = PauliX(wires=[3])
                self.y = PauliY(wires=[3])
                self.z = PauliZ(wires=[3])
                self.swap = SWAP(wires=[2,3])
                self.cz = CZ(wires=[2,3])
                self.cr = CR(has_params=True,trainable=True,wires=[2,3])
                self.rxx = RXX(has_params=True,trainable=True,wires=[2,3])
                self.rzz = RYY(has_params=True,trainable=True,wires=[2,3])
                self.ryy = RZZ(has_params=True,trainable=True,wires=[2,3])
                self.rzx = RZX(has_params=True,trainable=False, wires=[2,3])
                self.toffoli = Toffoli(wires=[2,3,4],use_dagger=True)
                self.h =Hadamard(wires=[1])


                self.tlayer = T(wires=1)
                self.cnot = CNOT(wires=[0, 1])
                self.measure = MeasureAll(obs={\'Z0\':2,\'Y3\':3} 
            )

            def forward(self, x, *args, **kwargs):
                self.qm.reset_states(x.shape[0])
                self.i(q_machine=self.qm)
                self.s(q_machine=self.qm)
                self.swap(q_machine=self.qm)
                self.cz(q_machine=self.qm)
                self.x(q_machine=self.qm)
                self.x1(q_machine=self.qm)
                self.y(q_machine=self.qm)

                self.z(q_machine=self.qm)

                self.ryy(q_machine=self.qm)
                self.rxx(q_machine=self.qm)
                self.rzz(q_machine=self.qm)
                self.rzx(q_machine=self.qm,params = x[:,[1]])
                self.cr(q_machine=self.qm)
                self.u1(q_machine=self.qm)
                self.u2(q_machine=self.qm)
                self.u3(q_machine=self.qm)
                self.rx_layer(params = x[:,[0]], q_machine=self.qm)
                self.cnot(q_machine=self.qm)
                self.h(q_machine=self.qm)

                self.ry_layer(params = x[:,[1]], q_machine=self.qm)
                self.tlayer(q_machine=self.qm)
                self.rz_layer(params = x[:,[2]], q_machine=self.qm)
                self.toffoli(q_machine=self.qm)
                rlt = self.measure(q_machine=self.qm)

                return rlt
            

        input_x = tensor.QTensor([[0.1, 0.2, 0.3]])

        input_x = tensor.broadcast_to(input_x,[2,3])

        input_x.requires_grad = True

        qunatum_model = QModel(num_wires=6, dtype=pyvqnet.kcomplex64)

        l = TorchHybirdVQCQpandaQVMLayer(qunatum_model,
                                "3047DE8A59764BEDAC9C3282093B16AF1",
                    6,
                    6,
                    pauli_str_dict={\'Z0\':2,\'Y3\':3},
                    shots = 1000,
                    name="",
            submit_kwargs={"test_qcloud_fake":True},
                    query_kwargs={})

        y = l(input_x)
        print(y)

        y.backward()
        print(input_x.grad)
    '''
    def __init__(self, vqc_module, qcloud_token: str, num_qubits: int, num_cubits: int, pauli_str_dict: list[dict] | dict | None = None, shots: int = 1000, name: str = '', diff_method: str = '', submit_kwargs: dict = {}, query_kwargs: dict = {}) -> None: ...
TorchHybirdVQCQpandaQVMLayer = HybirdVQCQpandaQVMLayer
