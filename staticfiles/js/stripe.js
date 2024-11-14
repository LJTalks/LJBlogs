<script>
            // Initialize Stripe with your public key
            const stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
            document.getElementById("checkout-button").addEventListener("click", async (e) => {
                e.preventDefault();
        
                // Make an AJAX POST request to create a checkout session
                const response = await fetch("{% url 'create_checkout_session' product.id %}", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": "{{ csrf_token }}"  // Include CSRF token for security
                    },
                });
        
                // Parse the response
                const session = await response.json();
        
                // Redirect to Stripe's checkout page
                const { error } = await stripe.redirectToCheckout({
                    sessionId: session.id
                });
        
                if (error) {
                    console.error("Stripe Checkout error:", error.message);
                }
            });
        </script>