
import tensorflow as tf
from tensorflow.keras import layers

class MoEBlock(layers.Layer):
    """
    A highly simplified Mixture-of-Experts layer.
    - `num_experts`: number of expert sub-networks
    - `k`: top-K experts to select for each sample
    - `expert_units`: dimension of each expert's Dense layer output
    """
    def __init__(self, num_experts=4, k=2, expert_units=128, **kwargs):
        super(MoEBlock, self).__init__(**kwargs)
        self.num_experts = num_experts
        self.k = k
        self.expert_units = expert_units

        # Create expert sub-layers (e.g., simple Dense layers as placeholders)
        self.experts = [
            layers.Dense(self.expert_units, activation='relu', name=f"expert_{i}")
            for i in range(num_experts)
        ]
        # Router: used to produce gating scores (logits)
        self.router = layers.Dense(self.num_experts, activation=None, name="router_logits")

    def call(self, inputs):
        """
        Inputs: [batch_size, feature_dim]
        1) Compute gating logits from router
        2) Select top-K experts per sample
        3) Apply each selected expert and combine their outputs
        """
        # [batch_size, num_experts]
        router_logits = self.router(inputs)

        # Softmax gating to get probabilities
        router_probs = tf.nn.softmax(router_logits, axis=-1)

        # Find top-K experts indices for each sample
        # shape(top_k_values) = [batch_size, k], shape(top_k_indices) = [batch_size, k]
        top_k_values, top_k_indices = tf.math.top_k(router_probs, k=self.k, sorted=True)

        # Prepare to gather from experts
        expert_outputs = []
        batch_size = tf.shape(inputs)[0]

        # We will accumulate the combined output for each sample
        combined_output = tf.zeros([batch_size, self.expert_units], dtype=inputs.dtype)

        for i in range(self.num_experts):
            # mask for which samples route to expert i
            # [batch_size]
            expert_mask = tf.cast(tf.equal(top_k_indices, i), inputs.dtype)  # mask among top_k
            # sum across the k dimension => shape [batch_size]
            expert_mask = tf.reduce_sum(expert_mask, axis=1)

            # Probability that a sample routes to expert i
            # shape [batch_size]
            prob_i = tf.gather(router_probs[:, i], tf.range(batch_size))

            # Only compute the expert output for relevant samples
            # For simplicity, we compute for all and multiply by mask
            expert_out = self.experts[i](inputs)  # [batch_size, expert_units]

            # Weighted by the gating probability and whether it's in the top-k
            # Note: top_k_values are the actual probabilities; we only multiply by the mask here
            weighted_out = tf.expand_dims(prob_i, -1) * expert_out

            # Zero out for samples that are not in the top-k for this expert
            weighted_out = weighted_out * tf.expand_dims(expert_mask, -1)

            # Add to the combined output
            combined_output += weighted_out

        return combined_output


class MLABlock(layers.Layer):
    """
    Simplified Multi-Head Latent Attention (MLA).
    We treat 'inputs' as a single latent vector for simplicity
    and create Q, K, V transformations with multiple heads.
    """
    def __init__(self, d_model=128, num_heads=4, **kwargs):
        super(MLABlock, self).__init__(**kwargs)
        self.d_model = d_model
        self.num_heads = num_heads

        # For simplicity, we define separate layers for Q, K, V
        self.wq = layers.Dense(d_model, name='q_dense')
        self.wk = layers.Dense(d_model, name='k_dense')
        self.wv = layers.Dense(d_model, name='v_dense')

        # Final projection after attention
        self.dense_out = layers.Dense(d_model, name='mla_output')

    def split_heads(self, x, batch_size):
        """
        Split the last dimension into (num_heads, depth).
        For example, shape (batch_size, d_model) -> (batch_size, num_heads, depth).
        """
        depth = self.d_model // self.num_heads
        x = tf.reshape(x, (batch_size, self.num_heads, depth))
        return x

    def call(self, inputs):
        """
        A simplistic multi-head self-attention over a single latent vector.
        For demonstration, we can treat 'inputs' as [batch_size, d_model].
        """
        batch_size = tf.shape(inputs)[0]

        # Project to Q, K, V
        q = self.wq(inputs)  # (batch_size, d_model)
        k = self.wk(inputs)
        v = self.wv(inputs)

        # Split heads
        q = self.split_heads(q, batch_size)  # (batch_size, num_heads, depth)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)

        # Scaled dot-product attention over each head
        depth = self.d_model // self.num_heads
        # (batch_size, num_heads, depth) @ (batch_size, num_heads, depth)^T is not well-defined,
        # so we do this in a broadcast way: multiply across batch dimension first
        # For demonstration, we do a simplistic 1D attention for each head
        qkT = tf.reduce_sum(q * k, axis=-1, keepdims=True)  # shape (batch_size, num_heads, 1)
        scale = tf.sqrt(tf.cast(depth, tf.float32))
        attention_scores = qkT / scale  # shape (batch_size, num_heads, 1)
        attention_weights = tf.nn.softmax(attention_scores, axis=-2)  # same shape

        # Multiply by V
        out = attention_weights * v  # (batch_size, num_heads, depth)

        # Combine heads back
        out = tf.reshape(out, (batch_size, self.num_heads * depth))

        # Final projection
        out = self.dense_out(out)  # (batch_size, d_model)
        return out


class DeepSeekBlock(layers.Layer):
    """
    Combines the MoEBlock and MLABlock:
    1) The input first goes through the MoEBlock
    2) The output is then passed into the MLABlock
    3) Output is returned
    """
    def __init__(self,
                 num_experts=4,
                 top_k=2,
                 expert_units=128,
                 d_model=128,
                 num_heads=4,
                 **kwargs):
        super(DeepSeekBlock, self).__init__(**kwargs)
        self.moe = MoEBlock(num_experts=num_experts, k=top_k, expert_units=expert_units)
        self.mla = MLABlock(d_model=d_model, num_heads=num_heads)

    def call(self, inputs):
        moe_out = self.moe(inputs)
        mla_out = self.mla(moe_out)
        return mla_out
