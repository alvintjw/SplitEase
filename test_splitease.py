from splitease import read_csv, calculate_total_amount, find_optimal_transfers

def test_read_csv(tmp_path):
    # Create a temporary CSV file
    csv_content = "Alice,Bob,Charlie\n100,200,300\n27,9,3\n"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    
    # Read the CSV file
    data = read_csv(csv_file)
    
    # Expected result
    expected_data = {
        'Alice': [100, 27],
        'Bob': [200, 9],
        'Charlie': [300, 3]
    }
    
    assert data == expected_data

def test_calculate_total_amount():
    data = {
        'Alice': [100, 27],
        'Bob': [200, 9],
        'Charlie': [300, 3]
    }
    
    total_amounts, average_payment = calculate_total_amount(data)
    
    expected_total_amounts = {
        'Alice': 127,
        'Bob': 209,
        'Charlie': 303
    }
    
    expected_average_payment = (127 + 209 + 303) / 3
    
    assert total_amounts == expected_total_amounts
    assert average_payment == expected_average_payment

def test_find_optimal_transfers():
    total_amounts = {
        'Alice': 127,
        'Bob': 209,
        'Charlie': 303
    }
    
    average_payment = (127 + 209 + 303) / 3
    
    instructions = find_optimal_transfers(total_amounts, average_payment)
    
    expected_instructions = [
        'Alice pays 86.0 to Charlie',
        'Bob pays 4.0 to Charlie'
    ]
    
    assert instructions == expected_instructions

