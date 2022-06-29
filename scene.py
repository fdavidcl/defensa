from manim import *

class AutoencoderDrawing(Scene):
    def play_queue(self):
        self.play(*self.animation_queue)
        self.clear_queue()

    def clear_queue(self):
        self.animation_queue.clear()
        

    def transform_many(self, l_from, l_to):
        for a, b in zip(l_from, l_to):
            self.animation_queue.append(Transform(a, b))
    
    def layer_objects(self, n_units=1, left=0, color=RED):
        nodes1 = [Circle(.5).set_color(color) for _ in range(n_units)]
        nodes = VGroup(*nodes1)
        middle = (n_units - 1)/2
        for i, n in enumerate(nodes1):
            n.shift(DOWN * (i - middle) * 1.2)
            n.shift(LEFT * 2 * left)

        self.animation_queue.append(Create(nodes, lag_ratio=self.node_lag))
        return nodes1
        
    def connect_layers(self, l1, l2):
        lines = VGroup(*[Line(start=n.get_right(), end=m.get_left()).set_color(BLACK) for m in l2 for n in l1])
        self.animation_queue.append(Create(lines, lag_ratio=self.connection_lag))
        return lines

    def build_net(self, *layers, colors=None):
        autoencoder_mobjects = {
            "layers": [],
            "connections": []
        }
        for i, units in enumerate(layers):
            autoencoder_mobjects["layers"].append(self.layer_objects(n_units=units, left=(len(layers)-1)/2.-i, color=RED if colors is None else colors[i]))
            if i > 0:
                autoencoder_mobjects["connections"].append(self.connect_layers(autoencoder_mobjects["layers"][i-1],autoencoder_mobjects["layers"][i]))
        return autoencoder_mobjects

    def construct(self):
        self.animation_queue = []
        self.node_lag = 0.2
        self.connection_lag = 0.2
        self.camera.background_color = WHITE

class Scorer(AutoencoderDrawing):
    def construct(self):
        super().construct()
        self.build_net(5, 3, 2, 3, 5, colors=[GREY, GREY, RED, GREY, GREY])
        self.play_queue()
        self.pause(1)

class CreateNet(AutoencoderDrawing):
    def construct(self):
        super().construct()
        self.node_lag = 0.5

        # create "variables" represented as columns in a table
        table = [Rectangle(width=0.9, height=2.0, grid_xstep=1.0, grid_ystep=0.5).set_color(BLACK) for _ in range(5)]
        for i, n in enumerate(table):
            n.shift(RIGHT * (i - 2))
        
        self.play(Create(table[2]))
        self.play(Create(table[1]), Create(table[3]))
        self.play(Create(table[0]), Create(table[4]))
        
        # transform those variables into a set of 5 nodes, the input layer
        layer1 = self.layer_objects(5, 1, GREEN)
        self.clear_queue()
        self.wait(1.)
        self.transform_many(table, layer1)
        self.play_queue()
        self.add(*layer1)

        # "copy" those nodes onto the final output layer
        self.wait(0.5)
        layer3 = table # use the nodes that were just transformed as last layer
        self.play(VGroup(*layer3).animate.shift(4 * RIGHT))
        
        # create a middle "encoding" layer
        self.wait(0.5)
        layer2 = self.layer_objects(2, 0, PURPLE)
        self.play_queue()

        # connect layers to create a neural network
        l12c = self.connect_layers(layer1, layer2)
        self.play_queue()
        l23c = self.connect_layers(layer2, layer3)
        self.play_queue()

        # fade out connections
        self.play(VGroup(*l12c, *l23c).animate.fade(1))#*[l.animate.fade(1) for l in l12c], *[l.animate.fade(1) for l in l23c])

        # separate input and output
        self.play(VGroup(*layer1).animate.shift(2*LEFT), VGroup(*layer3).animate.shift(2*RIGHT))
        
        # create more hidden layers
        layer4 = self.layer_objects(3, 1)
        layer5 = self.layer_objects(3, -1)
        self.play_queue()

        self.connect_layers(layer1, layer4)
        self.connect_layers(layer4, layer2)
        self.connect_layers(layer2, layer5)
        self.connect_layers(layer5, layer3)
        self.play_queue()



