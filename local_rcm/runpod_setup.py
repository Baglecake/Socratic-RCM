#!/usr/bin/env python3
"""
RunPod vLLM Endpoint Setup Helper

This script helps you:
1. Test connectivity to your RunPod endpoint
2. Verify the model is responding correctly
3. Get the correct URL format for the Streamlit app

Prerequisites:
1. Create a RunPod account at https://runpod.io
2. Deploy a Serverless vLLM endpoint:
   - Go to Serverless > + New Endpoint
   - Select "vLLM" template
   - Choose model: Qwen/Qwen2.5-7B-Instruct (or similar)
   - Deploy and wait for it to be ready
3. Get your API key from Settings > API Keys

Usage:
    python runpod_setup.py --endpoint-id YOUR_ENDPOINT_ID --api-key YOUR_API_KEY
    python runpod_setup.py --test-url "https://api.runpod.ai/v2/xxx/openai/v1" --api-key YOUR_API_KEY
"""

import argparse
import sys


def test_runpod_connection(base_url: str, api_key: str, model: str = "default"):
    """Test connection to RunPod vLLM endpoint"""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    print(f"\nTesting RunPod connection...")
    print(f"URL: {base_url}")
    print(f"Model: {model}")
    print("-" * 50)

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0
        )

        # Test with a simple completion
        print("Sending test message...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from RunPod!' in exactly those words."}
            ],
            max_tokens=50
        )

        result = response.choices[0].message.content
        print(f"\nResponse: {result}")
        print("\n" + "=" * 50)
        print("SUCCESS! RunPod endpoint is working correctly.")
        print("=" * 50)
        print(f"\nUse these settings in the Streamlit app:")
        print(f"  Endpoint URL: {base_url}")
        print(f"  Model: {model}")
        return True

    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("  1. Check that your endpoint is deployed and 'Ready'")
        print("  2. Verify your API key is correct")
        print("  3. Ensure the URL format is correct:")
        print("     https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/openai/v1")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test RunPod vLLM endpoint connectivity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Test with endpoint ID
    python runpod_setup.py --endpoint-id abc123xyz --api-key rp_xxxxxxxx

    # Test with full URL
    python runpod_setup.py --test-url "https://api.runpod.ai/v2/abc123xyz/openai/v1" --api-key rp_xxxxxxxx

    # Specify model name
    python runpod_setup.py --endpoint-id abc123xyz --api-key rp_xxxxxxxx --model "Qwen/Qwen2.5-7B-Instruct"
        """
    )

    parser.add_argument("--endpoint-id", help="Your RunPod endpoint ID")
    parser.add_argument("--test-url", help="Full endpoint URL to test")
    parser.add_argument("--api-key", required=True, help="Your RunPod API key")
    parser.add_argument("--model", default="default", help="Model name (default: 'default')")

    args = parser.parse_args()

    if args.test_url:
        base_url = args.test_url
    elif args.endpoint_id:
        base_url = f"https://api.runpod.ai/v2/{args.endpoint_id}/openai/v1"
    else:
        print("ERROR: Must provide either --endpoint-id or --test-url")
        parser.print_help()
        sys.exit(1)

    success = test_runpod_connection(base_url, args.api_key, args.model)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
