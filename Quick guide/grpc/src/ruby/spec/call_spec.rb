# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

require 'spec_helper'

include GRPC::Core::StatusCodes

describe GRPC::Core::WriteFlags do
  it 'should define the known write flag values' do
    m = GRPC::Core::WriteFlags
    expect(m.const_get(:BUFFER_HINT)).to_not be_nil
    expect(m.const_get(:NO_COMPRESS)).to_not be_nil
  end
end

describe GRPC::Core::RpcErrors do
  before(:each) do
    @known_types = {
      OK: 0,
      ERROR: 1,
      NOT_ON_SERVER: 2,
      NOT_ON_CLIENT: 3,
      ALREADY_ACCEPTED: 4,
      ALREADY_INVOKED: 5,
      NOT_INVOKED: 6,
      ALREADY_FINISHED: 7,
      TOO_MANY_OPERATIONS: 8,
      INVALID_FLAGS: 9,
      ErrorMessages: {
        0 => 'ok',
        1 => 'unknown error',
        2 => 'not available on a server',
        3 => 'not available on a client',
        4 => 'call is already accepted',
        5 => 'call is already invoked',
        6 => 'call is not yet invoked',
        7 => 'call is already finished',
        8 => 'outstanding read or write present',
        9 => 'a bad flag was given'
      }
    }
  end

  it 'should have symbols for all the known error codes' do
    m = GRPC::Core::RpcErrors
    syms_and_codes = m.constants.collect { |c| [c, m.const_get(c)] }
    expect(Hash[syms_and_codes]).to eq(@known_types)
  end
end

describe GRPC::Core::CallOps do
  before(:each) do
    @known_types = {
      SEND_INITIAL_METADATA: 0,
      SEND_MESSAGE: 1,
      SEND_CLOSE_FROM_CLIENT: 2,
      SEND_STATUS_FROM_SERVER: 3,
      RECV_INITIAL_METADATA: 4,
      RECV_MESSAGE: 5,
      RECV_STATUS_ON_CLIENT: 6,
      RECV_CLOSE_ON_SERVER: 7
    }
  end

  it 'should have symbols for all the known operation types' do
    m = GRPC::Core::CallOps
    syms_and_codes = m.constants.collect { |c| [c, m.const_get(c)] }
    expect(Hash[syms_and_codes]).to eq(@known_types)
  end
end

describe GRPC::Core::Call do
  let(:test_tag)  { Object.new }
  let(:fake_host) { 'localhost:10101' }

  before(:each) do
    @ch = GRPC::Core::Channel.new(fake_host, nil, :this_channel_is_insecure)
  end

  describe '#status' do
    it 'can save the status and read it back' do
      make_test_call do |call|
        sts = Struct::Status.new(OK, 'OK')
        expect { call.status = sts }.not_to raise_error
        expect(call.status).to eq(sts)
      end
    end

    it 'must be set to a status' do
      make_test_call do |call|
        bad_sts = Object.new
        expect { call.status = bad_sts }.to raise_error(TypeError)
      end
    end

    it 'can be set to nil' do
      make_test_call do |call|
        expect { call.status = nil }.not_to raise_error
      end
    end
  end

  describe '#metadata' do
    it 'can save the metadata hash and read it back' do
      make_test_call do |call|
        md = { 'k1' => 'v1',  'k2' => 'v2' }
        expect { call.metadata = md }.not_to raise_error
        expect(call.metadata).to be(md)
      end
    end

    it 'must be set with a hash' do
      make_test_call do |call|
        bad_md = Object.new
        expect { call.metadata = bad_md }.to raise_error(TypeError)
      end
    end

    it 'can be set to nil' do
      make_test_call do |call|
        expect { call.metadata = nil }.not_to raise_error
      end
    end
  end

  describe '#set_credentials!' do
    it 'can set a valid CallCredentials object' do
      make_test_call do |call|
        auth_proc = proc { { 'plugin_key' => 'plugin_value' } }
        creds = GRPC::Core::CallCredentials.new auth_proc
        expect { call.set_credentials! creds }.not_to raise_error
      end
    end
  end

  describe '#cancel' do
    it 'completes ok' do
      make_test_call do |call|
        expect { call.cancel }.not_to raise_error
      end
    end

    it 'completes ok when the call is closed' do
      make_test_call do |call|
        call.close
        expect { call.cancel }.not_to raise_error
      end
    end
  end

  describe '#cancel_with_status' do
    it 'completes ok' do
      make_test_call do |call|
        expect do
          call.cancel_with_status(0, 'test status')
        end.not_to raise_error
        expect do
          call.cancel_with_status(0, nil)
        end.to raise_error(TypeError)
      end
    end

    it 'completes ok when the call is closed' do
      make_test_call do |call|
        call.close
        expect do
          call.cancel_with_status(0, 'test status')
        end.not_to raise_error
      end
    end
  end

  def make_test_call
    call = @ch.create_call(nil, nil, 'phony_method', nil, deadline)
    yield call
    call.close
  end

  def deadline
    Time.now + 2  # in 2 seconds; arbitrary
  end
end
